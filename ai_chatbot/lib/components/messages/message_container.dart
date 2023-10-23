import 'package:flutter/material.dart';

class MessageContainer extends StatelessWidget {
  const MessageContainer({
    super.key,
    required this.role,
    required this.content,
    required this.chatbotName,
  });

  final String role;
  final String content;
  final String chatbotName;
  final Color color = const Color.fromARGB(255, 66, 69, 73);

  @override
  Widget build(BuildContext context) {
    final IconData icon;
    final String name;

    switch (role) {
      case 'user':
        name = "User";
        icon = Icons.face;
        break;
      case 'assistant':
        name = chatbotName;
        icon = Icons.computer;
        break;
      case 'system':
        name = "System";
        icon = Icons.settings;
        break;
      default:
        name = "ERROR";
        icon = Icons.error;
    }

    MessageHeader messageHeader = MessageHeader(icon: icon, text: name);
    MessageBody messageBody = MessageBody(text: content);

    return Align(
      child: Container(
        color: color,
        alignment: Alignment.topLeft,
        padding: const EdgeInsets.all(12.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [messageHeader, const SizedBox(height: 8), messageBody],
        ),
      ),
    );
  }
}

class MessageText extends StatelessWidget {
  const MessageText(
      {super.key,
      required this.text,
      required this.size,
      required this.fontWeight,
      required this.colour});

  final String text;
  final double size;
  final FontWeight fontWeight;
  final Color colour;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      textAlign: TextAlign.left,
      style: TextStyle(
        fontSize: size,
        fontWeight: fontWeight,
        color: colour,
      ),
    );
  }
}

class MessageHeader extends StatelessWidget {
  const MessageHeader({super.key, required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    final MessageText header = MessageText(
      text: text,
      size: 26,
      fontWeight: FontWeight.bold,
      colour: Colors.white,
    );

    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        CircleAvatar(
          backgroundColor: const Color.fromARGB(255, 30, 33, 36),
          radius: 16,
          child: Icon(icon, color: Colors.white, size: 20),
        ),
        const SizedBox(width: 8),
        header
      ],
    );
  }
}

class MessageBody extends StatelessWidget {
  const MessageBody({super.key, required this.text});

  final String text;

  @override
  Widget build(BuildContext context) {
    return MessageText(
      text: text,
      size: 16,
      fontWeight: FontWeight.normal,
      colour: Colors.white,
    );
  }
}
