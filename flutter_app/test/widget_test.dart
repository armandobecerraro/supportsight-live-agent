import 'package:flutter_test/flutter_test.dart';
import 'package:supportsight_live/main.dart';

void main() {
  testWidgets('App renders SupportSight title', (tester) async {
    await tester.pumpWidget(const SupportSightApp());
    expect(find.text('SupportSight Live'), findsOneWidget);
  });
}
