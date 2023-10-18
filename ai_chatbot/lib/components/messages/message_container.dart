import 'package:flutter/material.dart';

class MessageContainer extends StatelessWidget {
  const MessageContainer(
      {super.key, required this.role, required this.content});

  final String role;
  final String content;
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
        name = "AI";
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
    Text messageBody = Text(
      content,
      textAlign: TextAlign.left,
      style: const TextStyle(
        color: Colors.white,
        fontSize: 16.0,
      ),
    );

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

class MessageHeader extends StatelessWidget {
  const MessageHeader({super.key, required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        Icon(icon),
        const SizedBox(width: 8),
        Text(
          text,
          textAlign: TextAlign.left,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 24.0,
            fontWeight: FontWeight.bold,
          ),
        )
      ],
    );
  }
}
