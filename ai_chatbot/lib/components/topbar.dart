import 'package:flutter/material.dart';

class TopBar extends StatelessWidget implements PreferredSizeWidget {
  const TopBar({super.key, required this.title});

  final String title;

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: Text(title),
      backgroundColor: const Color.fromARGB(255, 40, 43, 48),
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}
