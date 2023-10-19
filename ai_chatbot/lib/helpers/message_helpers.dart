import 'package:ai_chatbot/providers/message_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MessageHelpers {
  static void sendMessage(MessageProvider messageProvider, String message) {
    messageProvider.addMessage({'role': 'user', 'content': message});
    MessageHelpers.postMessage(message)
        .then((_) => messageProvider.getMessages());
  }

  static Future<void> postMessage(String message) async {
    final url = Uri.parse('http://127.0.0.1:5000/api/messages');
    final body = jsonEncode({'message': message});
    final headers = {'Content-Type': 'application/json'};

    try {
      final response = jsonDecode(
          (await http.post(url, headers: headers, body: body)).body)["reply"];
      print(response);
    } catch (e) {
      print('Error: $e');
    }
  }
}
