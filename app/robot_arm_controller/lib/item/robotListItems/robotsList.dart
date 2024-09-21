import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/robotList/controlModeSelectionScreen.dart';

class RobotsList extends StatefulWidget {
  const RobotsList({super.key});

  @override
  State<RobotsList> createState() => _RobotsListState();
}

class _RobotsListState extends State<RobotsList> {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        GestureDetector(
          onTap: () {
            showModalBottomSheet(
              context: context,
              isScrollControlled: true,
              backgroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.only(
                      topRight: Radius.circular(25),
                      topLeft: Radius.circular(25)
                  )
              ),
              builder: (context) {
                return Container(
                  decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.only(
                          topLeft: Radius.circular(25.0),
                          topRight: Radius.circular(25.0)
                      )
                  ),
                  child: DraggableScrollableSheet(
                    expand: false,
                    builder: (context, scrollController) {
                      return ControlModeSclectionScreen(
                      );
                    },
                  ),
                );
              },
            );
          },
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.white,
            ),
            child: Padding(
              padding: EdgeInsets.fromLTRB(16, 30, 16, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.only(bottom: 12),
                    child: Stack(
                      children: [
                        ClipRRect(
                          borderRadius: BorderRadius.circular(16),
                          child: Image.asset(
                            'assets/openmani.jpg',
                            width: double.infinity,
                            height: 230,
                            fit: BoxFit.cover,
                          ),
                        ),
                        Positioned.fill(
                          child: Center(
                            child: Text(
                              'TEST',
                              style: TextStyle(
                                color: Colors.white, // 텍스트 색상을 이미지 위에서 잘 보이도록 설정
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                backgroundColor: Colors.black54, // 텍스트 배경을 반투명 검정색으로 설정
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }
}
