class User {
  final String employeeNumber;
  final String email;
  final String nickname;
  final String password;

  User({
    required this.employeeNumber,
    required this.email,
    required this.nickname,
    required this.password,
  });

  Map<String, dynamic> toJson() {
    return {
      'employeeNumber': employeeNumber,
      'email': email,
      'nickname': nickname,
      'password': password,
    };
  }
}