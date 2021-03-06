using Gee;

public class Main : Object {

  public static int main(string[] args) {
    try {
      new VWS.Options().parse(args);
      var ws = new VWS.Server();
      ws.start();
    } catch (Error e) {
      stderr.printf("%s\n", e.message);
    }
    return 0;
  }
}

namespace VWS {
  public class Server : Object {
    private SocketService ss;
    private MainLoop loop;

    public Server() throws Error {
      ss   = new SocketService();
      loop = new MainLoop();

      ss.listen_backlog = 1024;
      ss.add_inet_port(VWS.Options.port, null);
      ss.incoming.connect(on_connection);
    }

    private void ensure_backup_script() {
      try {
        File.new_for_path(VWS.Options.static_dir).make_directory();
      } catch (Error e) {}
      try {
        File.new_for_path(VWS.Options.static_dir + "b").make_directory();
        var backup_script = VWS.Options.static_dir + "b.sh";
        var f = File.new_for_path(backup_script);
        var fos = f.create(FileCreateFlags.PRIVATE);
        fos.write("""#!/usr/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
/usr/bin/gtar --no-recursion --force-local -cjf "b/$(/usr/gnu/bin/date -Iminutes -u).tar.bz2" *
cd b; /usr/gnu/bin/ls -1 | /usr/gnu/bin/sort | /usr/gnu/bin/head -n -10 | /usr/bin/xargs /usr/gnu/bin/rm
exit 0
""".data);
        FileUtils.chmod(backup_script, 0700);
      } catch (Error e) {
        stderr.printf("Can't create backup file: %s\n", e.message);
      }
    }

    public void start() {
      ensure_backup_script();
      ss.start();

      var ts = new TimeoutSource(VWS.Options.backup_timeout * 1000);
      ts.set_callback(() => {
        try {
          Process.spawn_command_line_async(VWS.Options.static_dir + "b.sh");
        } catch (SpawnError e) {
          stderr.printf ("Backup error: %s\n", e.message);
        }
        return true;
      });
      ts.attach(loop.get_context());
      loop.run();
    }

    private bool on_connection(SocketConnection connection) {
      connection.socket.timeout = VWS.Options.inactivity_timeout;
      process_request.begin(connection);
      return true;
    }

    private async void process_request(SocketConnection connection) {
      try {
        var tx = new Tx(
          new DataInputStream(connection.input_stream),
          new DataOutputStream(connection.output_stream)
        );
        yield tx.parse();

        if (tx.req.method == "GET") {
          var f = File.new_for_path(VWS.Options.static_dir + tx.req.url.path);
          yield tx.fix_headers(f);

          yield tx.write_start_line();
          yield tx.write_headers();
          yield tx.serve(f);
        } else if (tx.req.method == "HEAD") {
          var f = File.new_for_path(VWS.Options.static_dir + tx.req.url.path);
          yield tx.fix_headers(f);

          yield tx.write_start_line();
          yield tx.write_headers();
        } else if (tx.req.method == "PUT") {
          var f = File.new_for_path(VWS.Options.static_dir + tx.req.url.path);

          yield tx.save(f);
          yield tx.write_start_line();
          yield tx.write_headers();
        } else {
          tx.res.code = 501;

          yield tx.write_start_line();
          yield tx.write_headers();
        }
      } catch (Error e) {
        stderr.printf("Error while process socket: %s\n", e.message);
      }
    }
  }

  public class Tx : Object {
    public Request  req;
    public Response res;

    private DataInputStream  dis;
    private DataOutputStream dos;

    public Tx(DataInputStream dis, DataOutputStream dos) {
      this.dis = dis;
      this.dos = dos;

      req = new Request();
      res = new Response();

      // Initial headers
      res.headers.set("Server", "VWS");
      res.headers.set("Content-Type", "application/octet-stream");
      res.headers.set("X-Powered-By", "Vala 0.26.0");
      res.headers.set("Date", new DateTime.now_utc().to_string());
    }

    public async void parse() throws Error {
      MatchInfo mi;
      var start_line_re = new Regex("""
        ^([a-zA-Z]+)                                            # Method
        \s+([0-9a-zA-Z!#\$\%&'()*+,\-.\/:;=?\@[\\\]^_`\{|\}~]+) # URL
        \s+HTTP\/(\d\.\d)$                                      # Version
        """,
        RegexCompileFlags.EXTENDED
      );
      var header_line_re     = new Regex("""^(\S[^:]*)\s*:\s*(.*)$""");
      var ext_header_line_re = new Regex("""^\s+(.*)$""");

      // Read start line
      string line = yield dis.read_line_async(Priority.HIGH_IDLE);
      if (start_line_re.match(line, 0, out mi)) {
        this.req.method  = mi.fetch(1);
        this.req.version = mi.fetch(3);
        this.req.url     = new URL(mi.fetch(2));
      } else {
        return;
      }

      // Read headers
      string last_header_name = null;
      while (true) {
        line = yield dis.read_line_async(Priority.HIGH_IDLE);
        if (line == "" || line == "\r") break;

        if (header_line_re.match(line, 0, out mi)) {
          last_header_name = mi.fetch(1);
          this.req.headers.set(last_header_name, mi.fetch(2));

          if (last_header_name == "X-Ructfe") {
            this.res.headers.set(last_header_name, Hmac.compute_for_string(
              ChecksumType.SHA1, "RuCTFE_2014".data, mi.fetch(2))
            );
          }
        } else if (
          last_header_name != null &&
          ext_header_line_re.match(line, 0, out mi)
        ) {
          var v = this.req.headers.get(last_header_name);
          this.req.headers.set(last_header_name, v + mi.fetch(1));
        }
      }
    }

    public async void fix_headers(File f) throws Error {
      if (!f.query_exists() ||
        f.query_file_type(FileQueryInfoFlags.NONE) != FileType.REGULAR ) {
        this.res.code = 404;
        return;
      }

      var finfo = yield f.query_info_async("*",
        FileQueryInfoFlags.NONE, Priority.HIGH_IDLE);
      this.res.headers.set("Content-Length", finfo.get_size().to_string());
    }

    public async void serve(File f) throws Error {
      if (!this.res.headers.has_key("Content-Length")) return;

      var dis = new DataInputStream(f.read());
      while (true) {
        var bytes = yield dis.read_bytes_async(512, Priority.HIGH_IDLE);
        yield this.dos.write_bytes_async(bytes, Priority.HIGH_IDLE);
        if (bytes.length == 0) break;
      }
    }

    public async void save(File f) throws Error {
      if (!this.req.headers.has_key("Content-Length")) return;

      var fos = yield f.create_async(FileCreateFlags.PRIVATE,
        Priority.HIGH_IDLE);
      var dos = new DataOutputStream(fos);
      var len = int.parse(this.req.headers.get("Content-Length"));
      var count = 0;

      while (count < len) {
        var size = len - count < 512 ? len - count : 512;
        var bytes = yield this.dis.read_bytes_async(size, Priority.HIGH_IDLE);
        yield dos.write_bytes_async(bytes, Priority.HIGH_IDLE);
        count += bytes.length;
      }
    }

    public async void write_start_line() throws Error {
      var code = this.res.code.to_string();
      yield dos.write_async(@"HTTP/1.1 $code OK\n".data, Priority.HIGH_IDLE);
    }

    public async void write_headers() throws Error {
      foreach (var entry in res.headers.entries) {
        string name  = entry.key;
        string value = entry.value;
        yield dos.write_async(@"$name: $value\n".data, Priority.HIGH_IDLE);
      }
      yield dos.write_async("\n".data, Priority.HIGH_IDLE);
    }
  }

  public class URL : Object {
    public string scheme   { get; set; default = "http"; }
    public string path     { get; set; default = "/"; }
    public string query    { get; set; default = ""; }
    public string fragment { get; set; default = ""; }

    public URL(string url) {
      MatchInfo mi;
      try {
        var url_re = new Regex("""
          ^(([^:/?#]+):)?   # Scheme
          (//([^/?#]*))?    # Auth
          ([^?#]*)          # Path
          (\?([^#]*))?      # Query
          (\#(.*))?         # Fragment
        """, RegexCompileFlags.EXTENDED);

        if (url_re.match(url, 0, out mi)) {
          this.scheme   = mi.fetch(2);
          this.query    = mi.fetch(7);
          this.fragment = mi.fetch(9);

          var parts = mi.fetch(5).split("/");
          LinkedList<string> p = new LinkedList<string>();

          foreach (var part in parts) {
            if (part == "" || (part == ".." && p.size == 0)) continue;
            if (part == "..") p.poll_tail();
            else p.offer_tail(part);
          }
          foreach (var part in p)
            this.path += Uri.unescape_string(part) + "/";
          this.path = this.path.substring(0, this.path.length -1);
        }
      } catch (Error e) {}
    }
  }

  public class Message : Object {
    public string start_line { get; set; default = ""; }
    public HashMap<string, string> headers;

    public Message() {
      headers = new HashMap<string, string>();
    }
  }

  public class Request : Message {
    public string method    { get; set; }
    public URL url          { get; set; }
    public string version   { get; set; }
  }

  public class Response : Message {
    public uint16 code { get; set; default = 200; }
  }

  public class Options : Object {
    public static uint16 port = 3000;
    public static uint16 inactivity_timeout = 60;
    public static uint16 backup_timeout = 60;
    public static string static_dir = "./";

    private static const OptionEntry[] options = {
      {"port", 'p', 0, OptionArg.INT, ref port, "port (default 3000)", null},
      {"inactivity_timeout", 'i', 0, OptionArg.INT, ref inactivity_timeout,
        "inactivity timeout for connection (default 60s)", null},
      {"backup_timeout", 'b', 0, OptionArg.INT, ref backup_timeout,
        "timeout for periodical backup static dir (default 60s)", null},
      {"static_dir", 'd', 0, OptionArg.FILENAME, ref static_dir,
        "catalog for serving static files", null},
      {null}
    };

    public static void parse(string[] args) throws OptionError {
      var option_context = new OptionContext("Vala static web server");
      option_context.set_help_enabled(true);
      option_context.add_main_entries(options, null);
      option_context.parse(ref args);
    }
  }
}
