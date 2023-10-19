import 'package:flutter/material.dart';
import 'package:ai_chatbot/providers/message_provider.dart';
import 'package:ai_chatbot/helpers/message_helpers.dart';

class MessageInput extends StatefulWidget {
  const MessageInput({super.key, required this.messageProvider});

  final MessageProvider messageProvider;

  void _sendMessage(String message) {
    if (message != "") {
      MessageHelpers.sendMessage(messageProvider, message);
    }
  }

  @override
  MessageInputState createState() => MessageInputState();
}

class MessageInputState extends State<MessageInput> {
  final TextEditingController _messageController = TextEditingController();

  @override
  void dispose() {
    _messageController.dispose();
    super.dispose();
  }

  void sendMessage() {
    final messageContent = _messageController.text;
    widget._sendMessage(messageContent);

    // Clear the text field
    _messageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      color: const Color.fromARGB(255, 40, 43, 48),
      child: Row(
        children: [
          Expanded(
            child: MessageInputField(messageController: _messageController),
          ),
          const SizedBox(width: 16.0),
          IconButton(
            icon: const Icon(Icons.send, color: Colors.white),
            onPressed: sendMessage,
          ),
        ],
      ),
    );
  }
}

class MessageInputField extends StatelessWidget {
  const MessageInputField({super.key, required this.messageController});

  final TextEditingController messageController;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: messageController,
      autofocus: true,
      minLines: 1,
      maxLines: 5,
      style: const TextStyle(color: Colors.white),
      decoration: const InputDecoration(
        filled: true,
        fillColor: Color.fromARGB(255, 30, 33, 36),
        hintText: 'Type a message...',
        hintStyle: TextStyle(color: Colors.white),
        border: OutlineInputBorder(),
      ),
    );
  }
}
