using Gee;

public class Main : Object {

  public static int main(string[] args) {
    try {
      VWS.Options.parse(args);
      var ws = new VWS.Server();
      ws.start();
      stderr.printf("Server started at %d\n", VWS.Options.port);
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

    public void start() {
      ss.start();
      loop.run();
    }

    private bool on_connection(SocketConnection connection) {
      connection.socket.timeout = VWS.Options.inactivity_timeout;
      stdout.printf("Got incoming connection\n");
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
        this.req.url     = mi.fetch(2);
        this.req.version = mi.fetch(3);
      } else {
      }
      dos.put_string("Echo: %s\n".printf(line));

      // Read headers
      string last_header_name = null;
      while (true) {
        line = yield dis.read_line_async(Priority.HIGH_IDLE);
        if ((line ?? "") == "") break;

        if (header_line_re.match(line, 0, out mi)) {
          last_header_name = mi.fetch(1);
          this.req.headers.set(last_header_name, mi.fetch(2));
        } else if (
          last_header_name != null &&
          ext_header_line_re.match(line, 0, out mi)
        ) {
          var v = this.req.headers.get(last_header_name);
          this.req.headers.set(last_header_name, v + mi.fetch(1));
        }
      }

      foreach (var e in this.req.headers.entries) {
        stderr.printf("H = '%s' : '%s'\n", e.key, e.value);
      }

      // Read body
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
    public bool is_finished { get; set; default = false; }
    public string method    { get; set; }
    public string url       { get; set; }
    public string version   { get; set; }
  }

  public class Response : Message {
  }

  public class Options : Object {
    public static uint16 port = 3000;
    public static uint16 inactivity_timeout = 60;

    private static const OptionEntry[] options = {
      {"port", 'p', 0, OptionArg.INT, ref port, "port (default 3000)", null},
      {"inactivity_timeout", 'i', 0, OptionArg.INT, ref inactivity_timeout,
        "inactivity timeout for connection (default 60s)", null},
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
