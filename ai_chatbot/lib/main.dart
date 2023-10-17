import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'components/topbar.dart';
import 'providers/message_provider.dart';
import 'pages/chat_page.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => MessageProvider(),
      child: const MainApp(),
    ),
  );
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  MainAppState createState() => MainAppState();
}

class MainAppState extends State<MainApp> {
  @override
  void initState() {
    super.initState();
    final messageProvider =
        Provider.of<MessageProvider>(context, listen: false);
    messageProvider.getMessages();
  }

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        appBar: TopBar(
          title: "AI Chatbot",
        ),
        body: ChatPage(),
      ),
    );
  }
}
