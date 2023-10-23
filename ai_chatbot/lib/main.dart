import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/message_provider.dart';
import 'components/topbar.dart';
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

class MainAppState extends State<MainApp> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    final messageProvider =
        Provider.of<MessageProvider>(context, listen: false);
    messageProvider.getPersonalityConfig();
    messageProvider.loadMessages();
    messageProvider.getMessages();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final messageProvider =
        Provider.of<MessageProvider>(context, listen: false);
    if (state == AppLifecycleState.paused) {
      messageProvider.endChat();
    } else if (state == AppLifecycleState.resumed) {
      messageProvider.getMessages();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
          scaffoldBackgroundColor: const Color.fromARGB(255, 66, 69, 73)),
      home: const Scaffold(
        appBar: TopBar(
          title: "AI Chatbot",
        ),
        body: ChatPage(),
      ),
    );
  }
}
