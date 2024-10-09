import 'package:http/http.dart' as http;

class HttpService {
  final String url;

  HttpService(this.url);

  Future<String> sendRequest() async {
    try {
      final uri = Uri.parse(url);
      final response = await http.post(uri);
      if (response.statusCode == 200) {
        return '요청 성공!';
      } else {
        return '요청 실패: ${response.statusCode}';
      }
    } catch (e) {
      return '에러 발생: $e';
    }
  }
}