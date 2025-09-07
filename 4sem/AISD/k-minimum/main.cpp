#include <algorithm>
#include <iostream>
#include <vector>
#include <fstream>
#include <random>

using namespace std;

int cnt = 0;


int partition(vector<int> &arr, int l, int r, mt19937 &gen) {
    if (l != r) {
        uniform_int_distribution<> dis(l, r - 1);
        swap(arr[dis(gen)], arr[r]);
    }
    int x = arr[r];
    int i = l;
    for (int j = l; j < r; j++) {
        if (arr[j] <= x) {
            swap(arr[i], arr[j]);
            cnt++;
            i++;
        }
    }
    swap(arr[i], arr[r]);
    cnt++;
    return i;
}

int nth(vector<int> arr, int n, int size, mt19937 &gen) {
    int l = 0, r = size - 1;
    while (true) {
        int pos = partition(arr, l, r, gen);
        if (pos < n) {
            l = pos + 1;
        } else if (pos > n) {
            r = pos - 1;
        } else {
            return arr[n];
        }
    }
}

vector<int> generateRandomVector(int n, mt19937 &gen) {
    vector<int> arr(n);
    uniform_int_distribution<> dis(0, RAND_MAX);
    for (int i = 0; i < n; i++) {
        arr[i] = dis(gen);
    }
    std::sort(arr.begin(), arr.end(), [](int a, int b) -> bool { return a < b; });
    return arr;
}

int main() {
    const char *path = "data_antisorted.csv";
    ofstream fout(path);
    if (!fout.is_open()) {
        cerr << "Error opening file!" << endl;
        return 1;
    }

    fout << "size,cnt\n";

    random_device rd;
    mt19937 gen(rd());

    for (int i = 10; i <= 100000; i += 100) {
        int total_cnt = 0;
        for (int j = 0; j < 1000; ++j) {
            vector<int> v = generateRandomVector(i, gen);
            cnt = 0;
            nth(v, 2, i, gen);
            total_cnt += cnt;
        }
        fout << i << ',' << total_cnt / 1000 << std::endl;
        cout << "Size: " << i << " Average count: " << total_cnt / 1000 << endl;
    }

//    for (int i = 1000; i <= 1000000; i += 10000) {
//        vector<int> v = generateRandomVector(i, gen);
//        cnt = 0;
//        nth(v, 2, i, gen);
//        fout << i << ',' << cnt << '\n';
//        cout << "Size: " << i << " Count: " << cnt << endl;
//    }

    fout.close();
    return 0;
}