import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class MessageProvider extends ChangeNotifier {
  List<Map<String, dynamic>> _messages = [];
  List<Map<String, dynamic>> get messages => _messages;
  ScrollController scrollController = ScrollController();

  Future<void> loadMessages() async {
    final response =
        await http.get(Uri.parse('http://10.0.2.2:5000/api/chat/load'));

    if (response.statusCode == 200) {
      print('Chat loaded successfully!');
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  Future<void> getMessages() async {
    final response =
        await http.get(Uri.parse('http://10.0.2.2:5000/api/messages'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _messages = List<Map<String, dynamic>>.from(data["messages"]);
      notifyListeners();
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  Future<void> endChat() async {
    final response =
        await http.get(Uri.parse('http://10.0.2.2:5000/api/chat/end'));

    if (response.statusCode == 200) {
      print('Chat ended successfully!');
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  void addMessage(Map<String, dynamic> message) {
    _messages.add(message);
    notifyListeners();
  }

  void deleteMessage(int index) {
    _messages.removeAt(index);
    notifyListeners();
  }
}
