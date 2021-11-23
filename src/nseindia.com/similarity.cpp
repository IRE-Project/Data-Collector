// This file is mainly responsible for running bruteforce comparisons between company names of the
// 2 data sets - bse_raw and linkslist using edit distance
#include <bits/stdc++.h>
using namespace std;

/*
Returns the minimum of 3 numbers
@param x:
@param y:
@param z:
@returns: int - the minimum
*/
int min(int x, int y, int z) { return min(min(x, y), z); }

/*
Returns the edit distance between 2 given strings
@param str1: first string
@param str2: second string
@param m: length of first string
@param n: length of second string
@returns: int - the edit distance
*/
int editDistDP(string str1, string str2, int m, int n)
{
	int dp[m + 1][n + 1];

	for (int i = 0; i <= m; i++) {
		for (int j = 0; j <= n; j++) {
			if (i == 0)
				dp[i][j] = j;

			else if (j == 0)
				dp[i][j] = i;

			else if (str1[i - 1] == str2[j - 1])
				dp[i][j] = dp[i - 1][j - 1];

			else
				dp[i][j]
					= 1
					+ min(dp[i][j - 1],
							dp[i - 1][j],
							dp[i - 1][j - 1]);
		}
	}

	return dp[m][n];
}

// Driver code
int main()
{
    int nse_count, c_count;
    vector <string> name;
    vector <float> capital;
    vector <string> symbol;
    vector <string> c_name;
    vector <string> c_cin;
    float cap;
    string temp_ns, temp_ss;

    cin >> nse_count;
    for(int i = 0; i < nse_count; ++i)
    {
        cin >> temp_ns;
        cin >> cap;
        cin >> temp_ss;
        name.push_back(temp_ns);
        capital.push_back(cap);
        symbol.push_back(temp_ss);
    }

    cin >> c_count;
    for(int i = 0; i < c_count; ++i)
    {
        cin >> temp_ss;
        cin >> temp_ns;
        c_cin.push_back(temp_ss);
        c_name.push_back(temp_ns);
    }

    for(int i = 0; i < c_count; ++i)
    {
        cout << c_cin[i] << endl;
        cout << c_name[i] << endl;

        for(int j = 0; j < nse_count; ++j)
        {
            int ed = editDistDP(c_name[i], name[j], c_name[i].size(), name[j].size());
            float similarity = 100 * (1 - (float)ed / (float)c_name[i].size());
            if (similarity > 60)
            {
                cout << name[j] << endl;
                cout << capital[j] << endl;
                cout << symbol[j] << endl;
            }
        }
        cout << "--DONE--" << endl;

        cerr << "\rProgress: " << i;
    }

	return 0;
}
