require([
  'jquery',
  'utils',
  'tpl!templates/message.erb.html',
  'bootstrap4/collapse'
], function ($, utils, messageTemplate) {

  function ChatClient(path, $form, $messages) {
    this.$form = $form;
    this.$messages = $messages;
    this.username = "anonymous";

    $form.on('submit', this.messageSubmitHandler.bind(this));

    console.log("Connecting to server...");

    this.sock = new WebSocket(utils.qualifyWebsocketURL(path));
    this.sock.onopen = this.socketOpenHandler.bind(this);
    this.sock.onerror = this.socketErrorHandler.bind(this);
    this.sock.onmessage = this.messageReceiveHandler.bind(this);
  }

  ChatClient.prototype = {

    sendMessage: function (msg) {
      var s = JSON.stringify(msg);
      var blob = new Blob([s], {type: 'application/json'});
      this.sock.send(blob);
    },

    systemMessage: function (s) {
      var $msg = $(messageTemplate({
        cls: "system",
        author: "system",
        body: s
      }));
      this.$messages.append($msg);
    },

    parseCommand: function (s) {
      console.log("Parsing command: " + s);
      if (s.lastIndexOf("nick", 0) === 0) {
        this.username = s.substring(4, s.length).trim();
        console.log("Set username to: " + this.username);
      }
    },

    messageSubmitHandler: function (e) {
      e.preventDefault();
      e.stopPropagation();

      var $field = this.$form.find('input[type=text]');
      var body = $field.val();

      if (body.charAt(0) === "/") {
        this.parseCommand(body.substring(1, body.length));
        $field.val("");
        return;
      }

      console.log("author", this.username);
      console.log("body", body);

      var msg = {
        author: this.username,
        body: body
      };

      var $msg = $(messageTemplate({
        cls: "me",
        author: msg.author,
        body: msg.body
      }));

      this.$messages.append($msg);
      $field.val("");

      this.sendMessage(msg);
    },

    socketOpenHandler: function (e) {
      console.log("Connected.");
    },

    socketErrorHandler: function (e) {
      alert("Websocket error: " + e);
    },

    messageReceiveHandler: function (e) {
      var that = this,
          reader = new FileReader();
      reader.addEventListener("loadend", function () {
        var msg = JSON.parse(reader.result);
        console.log("Received message.", msg);
        var $msg = $(messageTemplate({
          cls: "other",
          author: msg.author,
          body: msg.body
        }));
        that.$messages.append($msg);
      });
      reader.readAsText(e.data);
    }
  }

  $(function () {
    if (!('WebSocket' in window)) {
      alert("This browser does not support WebSockets.");
    }

    var client = new ChatClient("/client", $('.form-message'), $('.messages'));

    console.log('Loaded typewriter/main.');
  });
});
