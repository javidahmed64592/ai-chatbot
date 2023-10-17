import 'package:flutter/material.dart';

class MessageContainer extends StatelessWidget {
  const MessageContainer(
      {super.key, required this.role, required this.content});

  final String role;
  final String content;

  @override
  Widget build(BuildContext context) {
    final Color color;

    switch (role) {
      case 'user':
        color = Colors.red;
        break;
      case 'assistant':
        color = Colors.green;
        break;
      case 'system':
        color = Colors.blue;
        break;
      default:
        color = Colors.black;
    }

    return Align(
      child: Container(
        color: color,
        alignment: Alignment.topLeft,
        padding: const EdgeInsets.all(12.0),
        child: Text(
          content,
          textAlign: TextAlign.left,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 16.0,
          ),
        ),
      ),
    );
  }
}
