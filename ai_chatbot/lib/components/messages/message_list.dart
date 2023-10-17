import 'package:flutter/material.dart';
import 'package:ai_chatbot/components/messages/message_container.dart';

class MessageList extends StatelessWidget {
  const MessageList({super.key, required this.messages});

  final List<Map<String, dynamic>> messages;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: messages.length,
      itemBuilder: (context, index) {
        return MessageContainer(
          role: messages[index]['role']!,
          content: messages[index]['content']!,
        );
      },
    );
  }
}
