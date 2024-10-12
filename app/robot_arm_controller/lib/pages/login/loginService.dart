import 'dart:convert';

import 'package:http/http.dart' as http;

class LoginService {
  final String? token;
  final int statusCode;
  final loginURL =
      'https://port-0-painting-dummy-lyqylohp8957ca6e.sel5.cloudtype.app/api/users/login';

  LoginService({required this.token, required this.statusCode});

  Future<LoginService> requestLogin(String employeeNumber, String password) async {
    final response = await http.post(
      Uri.parse(loginURL),
      body: jsonEncode({
        'email': employeeNumber,
        'password': password,
      }),
      headers: <String, String> {
        'Content-Type': 'application/json; charset=UTF-8',
      },
    );

    if (response.statusCode == 200) {
      final token = jsonDecode(response.body)['accessToken'];
      print(response.statusCode);
      return LoginService(token: token, statusCode: response.statusCode);
    } else {
      return LoginService(token: null, statusCode: response.statusCode);
    }
  }
}
