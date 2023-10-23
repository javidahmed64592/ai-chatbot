import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ai_chatbot/providers/message_provider.dart';
import 'package:ai_chatbot/components/messages/message_input.dart';
import 'package:ai_chatbot/components/messages/message_list.dart';

class ChatPage extends StatelessWidget {
  const ChatPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<MessageProvider>(
      builder: (context, messageProvider, _) {
        return Column(
          children: [
            Expanded(
              child: MessageList(
                messages: messageProvider.messages,
                scrollController: messageProvider.scrollController,
                chatbotName: messageProvider.personalityConfig["name"],
              ),
            ),
            MessageInput(messageProvider: messageProvider),
          ],
        );
      },
    );
  }
}
