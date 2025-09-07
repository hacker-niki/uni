'''long long calc(int t, int x, int y, int p) {
	int rounds = 0;
	int enemy = 0;
	while (y >= t){
		if (enemy >= x)return 1e9;
		y -= x - enemy;
		enemy = 0;
		if (y >= 0)enemy += p;
		rounds += 1;
	}
	while (y > 0) {
		if (x <= 0)return 1e9;
		if (y > x) {
			y -= x;
		}
		else {
			enemy -= x - y;
			y = 0;
		}
		x -= enemy;
		if (y > 0){
			enemy += p;
		}
		rounds += 1;
	}
	while (enemy > 0) {
		if (x <= 0)return 1e9;
		enemy -= x;
		if (enemy > 0) {
			x -= enemy;
		}
		rounds += 1;
	}
	return rounds;
}
void Task57() {
	long long x, y, p;
	cin >> x >> y >> p;
	long long ans = 1e9;
	for (long long t = 0; t < y + 2; t++) {
		ans = min(ans, calc(t, x, y, p));
	}
	if (ans == 1e9)cout << -1;
	else cout << ans;
}
int main() {
	Task57();
	return 0;
}'''