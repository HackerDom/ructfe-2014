public class Main : Object {

  public static int main(string[] args) {
    try {
      VWS.Options.parse(args);
      var ws = new VWS.Server();
      ws.start();
      stderr.printf ("Server started at %d\n", VWS.Options.port);
    } catch (Error e) {
      stderr.printf ("%s\n", e.message);
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
        var dis = new DataInputStream(connection.input_stream);
        var dos = new DataOutputStream(connection.output_stream);

        while (true) {
          string data = yield dis.read_line_async(Priority.HIGH_IDLE);
          dos.put_string("Echo: %s\n".printf(data));
        }
      } catch (Error e) {
        stderr.printf("Error while process socket: %s\n", e.message);
      }
    }
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
