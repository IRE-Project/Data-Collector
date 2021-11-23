// This file is mainly responsible for running bruteforce comparisons between company names of the
// 2 data sets - bse_raw and linkslist
#include <bits/stdc++.h>
using namespace std;

// Driver code
int main()
{
    int bse_count, c_count, gcount  = 0;
    vector <int> sec_code;
    vector <string> name;
    vector <string> c_name;
    vector <string> c_cin;
    float cap;
    int sec_;
    string temp_ns, temp_ss;

    cin >> bse_count;
    for(int i = 0; i < bse_count; ++i)
    {
        cin >> sec_;
        cin >> temp_ns;
        name.push_back(temp_ns);
        sec_code.push_back(sec_);
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

        for(int j = 0; j < bse_count; ++j)
        {
//            int ed = editDistDP(c_name[i], name[j], c_name[i].size(), name[j].size());
//            float similarity = 100 * (1 - (float)ed / (float)c_name[i].size());
//            if (similarity > 70)
            if (c_name[i] == name[j])
            {
                cout << sec_code[j] << endl;
                cout << name[j] << endl;
                gcount++;
            }
        }
        cout << "--DONE--" << endl;

        cerr << "\rProgress: " << i;
    }
    cerr << "\n" << gcount << endl;
	return 0;
}
