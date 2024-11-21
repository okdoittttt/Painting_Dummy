import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:robot_arm_controller/pages/automode/autoMode.dart';
import 'package:robot_arm_controller/pages/manualmode/appControlURL.dart';
import 'package:robot_arm_controller/pages/manualmode/getIP.dart';
import 'package:robot_arm_controller/pages/manualmode/manualMode.dart';

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
                  backgroundColor: Colors.orange,
                  // shape:
                  //     RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                  minimumSize: Size(240, 50)),
              child: Text("자동 모드 선택",
                  style: TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold)),
            ),
            SizedBox(
              height: 10,
            ),
            ElevatedButton(
              onPressed: () {
                showModalBottomSheet(
                    context: context,
                    builder: (context) {
                      return Container(
                        decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.only(
                                topRight: Radius.circular(25.0),
                                topLeft: Radius.circular(25.0))),
                        child: DraggableScrollableSheet(
                          expand: false,
                          builder: (context, scrollController) {
                            return ChangeNotifierProvider(create: (context) => BaseUrlProvider(),
                            child: GetIP(),);
                          },
                        ),
                      );
                    });
              },
              style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange,
                  // shape:
                  //     RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                  minimumSize: Size(240, 50)),
              child: Text(
                "수동 모드 선택",
                style:
                    TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
