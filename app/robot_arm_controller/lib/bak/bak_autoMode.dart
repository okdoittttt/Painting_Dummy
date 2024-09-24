import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/robotList/controlModeSelectionScreen.dart';
import 'package:robot_arm_controller/pages/robotList/robotsconnectionScreen.dart';

class AutoMode extends StatefulWidget {
  const AutoMode({super.key});

  @override
  State<AutoMode> createState() => _AutoModeState();
}

class _AutoModeState extends State<AutoMode> {
  // 로봇 데이터를 받은 후 아래 화면에 사용
  String robotsName = 'TEST';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        //
        backgroundColor: Colors.white,
        automaticallyImplyLeading: false,
        title: Text('$robotsName 연결중 ...'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
                onPressed: () {
                  // todo 로봇에게 자동 제어 시작 명령
                },
                style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.black,
                    backgroundColor: Colors.grey,
                    shape:
                    RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                    minimumSize: Size(240, 50)),
                child: Text('자동 제어 시작')),
            SizedBox(
              height: 10,
            ),
            ElevatedButton(
                onPressed: () {
                  // todo 동작을 멈추고 초기화 하는 명령
                },
                style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.black,
                    backgroundColor: Colors.grey,
                    shape:
                    RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                    minimumSize: Size((240), 50)),
                child: Text('동작 초기화')),
            SizedBox(
              height: 10,
            ),
            ElevatedButton(
                onPressed: () {
                  // todo 로봇과의 연결을 해제함
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => RobotsconnectionScreen()));
                },
                style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.black,
                    backgroundColor: Colors.grey,
                    shape:
                    RoundedRectangleBorder(borderRadius: BorderRadius.zero),
                    minimumSize: Size((240), 50)),
                child: Text('연결 해제')),
            SizedBox(
              height: 300,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                    onPressed: () {
                      // todo 모드 선택 창으로 이동
                      showModalBottomSheet(context: context,
                          isScrollControlled: true,
                          builder: (context) {
                            return DraggableScrollableSheet(
                              expand: false,
                              builder: (context, scrollController) {
                                return ControlModeSclectionScreen();
                              },
                            );
                          });
                    },
                    style: ElevatedButton.styleFrom(
                        foregroundColor: Colors.black,
                        backgroundColor: Colors.grey,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.zero),
                        minimumSize: Size(180, 50)),
                    child: Text('자동/수동 모드 선택')),
                SizedBox(
                  width: 30,
                ),
                ElevatedButton(
                    onPressed: () {
                      // todo 수동 제어 모드로 이동
                    },
                    style: ElevatedButton.styleFrom(
                        foregroundColor: Colors.black,
                        backgroundColor: Colors.grey,
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.zero),
                        minimumSize: Size(180, 50)),
                    child: Text('수동 제어 모드 이동'))
              ],
            )
          ],
        ),
      ),
    );
  }
}
