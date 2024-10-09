import 'package:flutter/material.dart';
import 'package:robot_arm_controller/pages/join/joinService.dart';
import 'package:robot_arm_controller/pages/login/login.dart';

class JoinPage extends StatefulWidget {
  const JoinPage({super.key});

  @override
  State<JoinPage> createState() => _JoinPageState();
}

class _JoinPageState extends State<JoinPage> {
  String employeeNumber = '';
  String password = '';
  String nickname = '';
  String email = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFF4B39EF),
      body: Container(
        width: MediaQuery.sizeOf(context).width,
        height: MediaQuery.sizeOf(context).height * 1,
        decoration: BoxDecoration(
            image: DecorationImage(
                fit: BoxFit.cover,
                image: Image.asset(
                  'assets/ship3.jpg',
                ).image)),
        child: Column(
          mainAxisSize: MainAxisSize.max,
          children: [
            Container(
              width: double.infinity,
              height: 780,
              decoration: BoxDecoration(
                  color: Colors.white,
                  boxShadow: [
                    BoxShadow(
                        blurRadius: 7,
                        color: Color(0x4D090F13),
                        offset: Offset(0, 3))
                  ],
                  borderRadius: BorderRadius.only(
                      bottomLeft: Radius.circular(16),
                      bottomRight: Radius.circular(16),
                      topLeft: Radius.circular(0),
                      topRight: Radius.circular(0))),
              child: Padding(
                padding: EdgeInsetsDirectional.fromSTEB(20, 0, 20, 0),
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      SizedBox(
                        height: 30,
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 56, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Row(
                              children: [
                                Text(
                                  'JOIN',
                                  style: TextStyle(
                                      fontSize: 31,
                                      fontWeight: FontWeight.w900,
                                      color: Colors.orange),
                                ),
                                SizedBox(
                                  width: 9,
                                )
                              ],
                            )
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 10, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              'Please enter your information.',
                              style: TextStyle(fontSize: 15),
                            )
                          ],
                        ),
                      ),
                      SizedBox(
                        height: 30,
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.text,
                                onChanged: (val) {
                                  setState(() {
                                    employeeNumber = val;
                                  });
                                },
                                decoration: InputDecoration(
                                  labelText: 'Employee number',
                                  hintText:
                                      'Enter your Employee number here...',
                                  labelStyle: TextStyle(
                                      color: Colors.black), // 레이블 텍스트 색상
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.orange), // 포커스 시 테두리 색상
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.grey), // 비활성화 시 테두리 색상
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.visiblePassword,
                                onChanged: (val) {
                                  setState(() {
                                    password = val;
                                  });
                                },
                                obscureText: true,
                                decoration: InputDecoration(
                                  labelText: 'Password',
                                  hintText: 'Enter your password here...',
                                  labelStyle: TextStyle(
                                      color: Colors.black), // 레이블 텍스트 색상
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.orange), // 포커스 시 테두리 색상
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.grey), // 비활성화 시 테두리 색상
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.visiblePassword,
                                obscureText: true,
                                decoration: InputDecoration(
                                  labelText: 'Password check',
                                  hintText: 'Enter your password here...',
                                  labelStyle: TextStyle(
                                      color: Colors.black), // 레이블 텍스트 색상
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.orange), // 포커스 시 테두리 색상
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.grey), // 비활성화 시 테두리 색상
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.text,
                                onChanged: (val) {
                                  setState(() {
                                    nickname = val;
                                  });
                                },
                                decoration: InputDecoration(
                                  labelText: 'Name',
                                  hintText: 'Enter your Name here...',
                                  labelStyle: TextStyle(
                                      color: Colors.black), // 레이블 텍스트 색상
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.orange), // 포커스 시 테두리 색상
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.grey), // 비활성화 시 테두리 색상
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 16, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: TextFormField(
                                keyboardType: TextInputType.emailAddress,
                                onChanged: (val) {
                                  setState(() {
                                    email = val;
                                  });
                                },
                                decoration: InputDecoration(
                                  labelText: 'Email',
                                  hintText: 'Enter your Email here...',
                                  labelStyle: TextStyle(
                                      color: Colors.black), // 레이블 텍스트 색상
                                  focusedBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.orange), // 포커스 시 테두리 색상
                                  ),
                                  enabledBorder: OutlineInputBorder(
                                    borderSide: BorderSide(
                                        color: Colors.grey), // 비활성화 시 테두리 색상
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 24, 0, 0),
                        child: Row(
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              flex: 5, // 첫 번째 버튼의 비율
                              child: ElevatedButton(
                                onPressed: () {
                                  Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                          builder: (context) => LoginPage()));
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.transparent,
                                  foregroundColor: Colors.black,
                                  elevation: 0,
                                ),
                                child: Text(
                                  "Already have an account? Login",
                                  style: TextStyle(color: Colors.grey),
                                ),
                              ),
                            ),
                            SizedBox(width: 16), // 간격 조절을 위한 SizedBox 추가
                            Expanded(
                              flex: 5,
                              child: ElevatedButton(
                                onPressed: () {
                                  // Navigator.push(context, MaterialPageRoute(builder: (context) => RobotsconnectionScreen()));
                                  JoinService joinservice = JoinService();
                                  joinservice.signUp(employeeNumber, email,
                                      nickname, password);
                                },
                                style: ElevatedButton.styleFrom(
                                  backgroundColor:
                                      Colors.orange, // 배경색을 파란색으로 설정
                                  foregroundColor:
                                      Colors.white, // 텍스트 색상을 흰색으로 설정
                                  textStyle: TextStyle(
                                      fontWeight:
                                          FontWeight.w900), // 글자를 굵게(볼드) 설정
                                ),
                                child: Text("Join"),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            )
          ],
        ),
      ),
    );
  }
}
