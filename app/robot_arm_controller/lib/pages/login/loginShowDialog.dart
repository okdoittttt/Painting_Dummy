// import 'package:flutter/material.dart';
//
// class LoginShowDialog extends StatefulWidget {
//   const LoginShowDialog({super.key});
//
//   @override
//   State<LoginShowDialog> createState() => _LoginShowDialogState();
// }
//
// class _LoginShowDialogState extends State<LoginShowDialog> {
//   @override
//   Widget build(BuildContext context) {
//     return showDialog(
//       context: context,
//       builder: (context) => AlertDialog(
//         shape: RoundedRectangleBorder(
//           borderRadius: BorderRadius.circular(10),
//         ),
//         backgroundColor: Colors.orange,
//         title: Text(
//           '로그인 실패',
//           textAlign: TextAlign.center,
//           style: TextStyle(
//             fontSize: 20,
//             fontWeight: FontWeight.bold,
//             color: Colors.white,
//           ),
//         ),
//         content: Text(
//           ''
//               '회원 정보가 정확하지 않습니다.',
//           style: TextStyle(color: Colors.white),
//           textAlign: TextAlign.center,
//         ),
//         actions: [
//           TextButton(
//               onPressed: () {
//                 Navigator.pop(context);
//               },
//               child: Text('확인'))
//         ],
//       ),
//     );
//   }
// }
