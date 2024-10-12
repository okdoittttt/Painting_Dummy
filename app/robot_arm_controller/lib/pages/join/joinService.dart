import 'dart:convert';

import 'package:robot_arm_controller/pages/join/user.dart';
import 'package:http/http.dart' as http;

class JoinService {
  Future<int> signUp(String employeeNumber, String email, String nickname,
      String password) async {
    final user = User(
        employeeNumber: employeeNumber,
        email: email,
        nickname: nickname,
        password: password);

    final signUpURL =
        'https://port-0-painting-dummy-lyqylohp8957ca6e.sel5.cloudtype.app/api/users/signup';

    try {
      final response = await http.post(
        Uri.parse(signUpURL),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(user.toJson()),
      );

      if (response.statusCode == 200) {
        return response.statusCode;
      } else {
        return response.statusCode;
      }
    } catch (e) {
      return 400;
    }
  }
}
