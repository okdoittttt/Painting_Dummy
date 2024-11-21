import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';
import 'package:robot_arm_controller/pages/manualmode/manualMode.dart';

class GetIP extends StatefulWidget {
  const GetIP({super.key});

  @override
  State<GetIP> createState() => _GetIPState();
}

class _GetIPState extends State<GetIP> {
  final TextEditingController _textController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        automaticallyImplyLeading: false,
        title: Text('Enter IP'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _textController,
              decoration: InputDecoration(
                  border: OutlineInputBorder(), labelText: '172.12.45.478'),
            ),
            SizedBox(
              height: 50,
            ),
            ElevatedButton(
                onPressed: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => ManualMode(
                                baseURL: _textController.text,
                              )));
                },
                style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange, minimumSize: Size(240, 50)),
                child: Text('DECIDE'))
          ],
        ),
      ),
    );
  }
}
