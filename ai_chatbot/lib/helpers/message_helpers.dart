import 'package:ai_chatbot/providers/message_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MessageHelpers {
  static void sendMessage(MessageProvider messageProvider, String message) {
    messageProvider.addMessage({'role': 'user', 'content': message});
    String reply = "";

    // Send message via post request to get response
    Future<void> postData() async {
      final url = Uri.parse('http://127.0.0.1:5000/api/messages');
      final body = jsonEncode({'message': message});
      final headers = {'Content-Type': 'application/json'};

      try {
        final response = await http.post(url, headers: headers, body: body);

        if (response.statusCode == 200) {
          reply = jsonDecode(response.body)["reply"];
        } else {
          reply = 'Error - ${response.statusCode}';
        }
      } catch (e) {
        print('Error: $e');
      } finally {
        if (reply != "") {
          messageProvider.addMessage({'role': 'assistant', 'content': reply});
        }
      }
    }

    postData();
  }
}
