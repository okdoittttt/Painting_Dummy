import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/robotList/controlModeSelectionScreen.dart';

class RobotsList extends StatefulWidget {
  const RobotsList({super.key});

  @override
  State<RobotsList> createState() => _RobotsListState();
}

class _RobotsListState extends State<RobotsList> {
  var robotsName = 'Open Manipulator-X';

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
                      topLeft: Radius.circular(25))),
              builder: (context) {
                return Container(
                  decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.only(
                          topLeft: Radius.circular(25.0),
                          topRight: Radius.circular(25.0))),
                  child: DraggableScrollableSheet(
                    expand: false,
                    builder: (context, scrollController) {
                      return ControlModeSclectionScreen();
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
              padding: EdgeInsets.fromLTRB(16, 25, 16, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.only(bottom: 12),
                    child: Container(
                      decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.withOpacity(0.8), width: 3),
                          borderRadius: BorderRadius.circular(16)),
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
                          Positioned(
                            bottom: 0,
                            left: 0,
                            right: 0,
                            child: Container(
                              padding: EdgeInsets.all(8.0),
                              decoration: BoxDecoration(
                                  color: Colors.orange,
                                  borderRadius: BorderRadius.only(
                                    bottomRight: Radius.circular(13),
                                    bottomLeft: Radius.circular(13),
                                  )),
                              child: Center(
                                child: Text(
                                  robotsName,
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 24,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
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
