import 'package:flutter/material.dart';
import 'package:ai_chatbot/components/messages/message_container.dart';

class MessageList extends StatelessWidget {
  const MessageList(
      {super.key, required this.messages, required this.scrollController});

  final List<Map<String, dynamic>> messages;
  final ScrollController scrollController;

  void scrollToBottom(ScrollController scrollController) {
    scrollController.animateTo(
      scrollController.position.maxScrollExtent,
      duration: const Duration(milliseconds: 300),
      curve: Curves.elasticOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    WidgetsBinding.instance
        .addPostFrameCallback((_) => scrollToBottom(scrollController));

    return ListView.builder(
      controller: scrollController,
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
