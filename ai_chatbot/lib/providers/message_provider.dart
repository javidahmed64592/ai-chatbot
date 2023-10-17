import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class MessageProvider extends ChangeNotifier {
  List<Map<String, dynamic>> _messages = [];

  Future<void> getMessages() async {
    final response =
        await http.get(Uri.parse('http://127.0.0.1:5000/api/messages'));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _messages = List<Map<String, dynamic>>.from(data["messages"]);
      notifyListeners();
    } else {
      throw Exception('Failed to fetch messages');
    }
  }

  List<Map<String, dynamic>> get messages => _messages;

  void addMessage(Map<String, dynamic> message) {
    _messages.add(message);
    notifyListeners();
  }

  void deleteMessage(int index) {
    _messages.removeAt(index);
    notifyListeners();
  }
}
