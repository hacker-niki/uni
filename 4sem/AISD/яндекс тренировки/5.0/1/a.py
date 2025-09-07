'''#include <iostream>
#include <string>
#include <map>
#include <stack>
#include <set>
#include <vector>
#include <iterator>
#include <fstream>
#include <algorithm>
#include <cmath>
#include <random>
#include <iomanip>

using namespace std;

void y51() {
	int p, v, q, m;
	cin >> p >> v >> q >> m;
	if ((q - m >= p - v && q - m <= p + v) || (q + m >= p - v && q + m <= p + v) || (p + v >= q - m && p + v <= q + m) || (p - v >= q - m && p - v <= q + m)) {
		cout << max(p + v, q + m) - min(p - v, q - m) + 1;
	}
	else {
		cout << 2 * (v + m + 1);
	}
}
int main()
{
	y51();
	return 0;
}'''