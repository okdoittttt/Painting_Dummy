import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/automode/autoMode.dart';

class ControlModeSclectionScreen extends StatelessWidget {
  const ControlModeSclectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        automaticallyImplyLeading: false,
        title: Text('Select Mode'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, // 세로 방향의 정렬을 중앙에 배치
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => AutoMode()),
                );
              },
              style: ElevatedButton.styleFrom(
                foregroundColor: Colors.black,
                backgroundColor: Colors.grey,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.zero
                ), minimumSize: Size(240, 50)
              ),
              child: Text("자동 모드 선택"),
            ),
            SizedBox(height: 10,),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                  foregroundColor: Colors.black,
                  backgroundColor: Colors.grey,
                  shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.zero
                  ), minimumSize: Size(240, 50)
              ),
              child: Text("수동 모드 선택"),
            ),
          ],
        ),
      ),
    );
  }
}
