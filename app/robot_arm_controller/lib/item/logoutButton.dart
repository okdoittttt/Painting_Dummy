import 'package:flutter/material.dart';

class LogoutButton extends StatelessWidget {
  const LogoutButton({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {},
      style: ElevatedButton.styleFrom(
          foregroundColor: Colors.black,
          backgroundColor: Colors.grey,
          shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.zero),
          minimumSize: Size(100, 50)
      ),
      child: Text('Logout'),
    );
  }
}
