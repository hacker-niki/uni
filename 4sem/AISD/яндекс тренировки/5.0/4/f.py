 #include <iostream>
 #include <vector>
 #include <algorithm>
 using namespace std;

 int w, h, n;
 vector<pair<int, int>> a;
 vector<int> prefmin, prefmax, sufmin, sufmax;

 bool check(int m) {
     int r = 0;
     int pmx = -1e9;
     int pmn = 1e9;
     for (int i = 0; i < n; i++) {
         while (r < n && a[r].first < a[i].first + m) {
             r++;
         }
         int mx = pmx;
         int mn = pmn;
         if (r != n) {
             mx = max(mx, sufmax[r]);
             mn = min(mn, sufmin[r]);
         }
         if (mx - mn < m) {
             return true;
         }
         pmx = prefmax[i];
         pmn = prefmin[i];
     }
     return false;
 }

 int main() {
     cin >> w >> h >> n;
     a.resize(n);
     for (int i = 0; i < n; i++) {
         cin >> a[i].first >> a[i].second;
     }
     sort(a.begin(), a.end());

     prefmin.resize(n, a[0].second);
     prefmax.resize(n, a[0].second);
     sufmin.resize(n, a[n-1].second);
     sufmax.resize(n, a[n-1].second);

     for (int i = 1; i < n; i++) {
         prefmin[i] = min(prefmin[i-1], a[i].second);
         prefmax[i] = max(prefmax[i-1], a[i].second);
     }

     for (int i = n-2; i >= 0; i--) {
         sufmin[i] = min(sufmin[i+1], a[i].second);
         sufmax[i] = max(sufmax[i+1], a[i].second);
     }

     int l = 0;
     int r = min(w, h);
     while (l < r) {
         int m = (l + r) / 2;
         if (check(m)) {
             r = m;
         } else {
             l = m + 1;
         }
     }
     cout << l << endl;
     return 0;
 }
