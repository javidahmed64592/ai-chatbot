import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class MessageProvider extends ChangeNotifier {
  List<Map<String, dynamic>> _messages = [];
  List<Map<String, dynamic>> get messages => _messages;
  ScrollController scrollController = ScrollController();

  Future<void> loadMessages() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chat/load');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      print('Chat loaded successfully!');
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  Future<void> getMessages() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/messages');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _messages = List<Map<String, dynamic>>.from(data["messages"]);
      notifyListeners();
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  Future<void> endChat() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chat/end');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      print('Chat ended successfully!');
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  void sendMessage(String message) {
    postMessage(message).then((_) => getMessages());
    getReply().then((_) => getMessages());
  }

  Future<void> postMessage(String message) async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chat/send');
    final body = jsonEncode({'message': message});
    final headers = {'Content-Type': 'application/json'};

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      print(jsonDecode(response.body));
    } else {
      throw Exception('Failed to send message');
    }
  }

  Future<void> getReply() async {
    final url = Uri.parse('http://10.0.2.2:5000/api/chat/reply');
    final response = await http.get(url);

    if (response.statusCode == 200) {
      print(jsonDecode(response.body));
    } else {
      throw Exception('Failed to generate reply');
    }
  }
}
