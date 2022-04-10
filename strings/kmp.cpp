#include <bits/stdc++.h>
using namespace std;


// the kmp pi array function;
vector<int> get_pi_array(const string& s){
	int n = s.size();
	vector<int> pi(n);
	for (int i=1; i<n; i++){
		if (s[i] == s[pi[i-1]])
			pi[i] = pi[i-1] + 1;
		else{
			int k = pi[i-1];
			while (k > 0 && s[i] != s[k])
				k = pi[k-1];
			if (k > 0)
				pi[i] = k + 1;
			else if (s[i] != s[k])
				pi[i] = 0;
			else
				pi[i] = 1;
		}
	}
	return pi;
}


// find the first index of every occurrance of s in t;
vector<int> kmp(const string& s, const string& t){
	/* 
	Say s is of length n and t is of length m;
	Imagine you had the single string big_string = s + <unique_token> + t,
	where <unique_token> cannot be found in either s or t;

	Then if you calculate the pi_array for big_string,
	whenever you get a value of n for an entry in t, that
	means that you have found a full occurance of s in t;

	This is the case because pi[i] <= pi[i-1] + 1 and the value
	of pi[n] = 0 since that corresponds to the slot of <unique_token>.
	i.e. the longest prefix that is also a suffix of big_string[0:n] is 0
	since <unique_token> occurs only once in big_string[0:n];

	Once we find an occurance though, we don't start comparing chars
	from the start, but actually we check the length of the longest
	prefix that is also a suffix of big_string[0:n-1] (i.e., s);
	This is because "bobo" appears 2 times in "bobobo"; If we had
	started from the start instead, we would find only one occurrance of "bobo";

	If we know that max(pi_array) <= n, we can only store n+1 values
	(for s and the <unique_token>) and then we continue with the
	calculation of the pi_array values of the remaining string in
	an online fashion (i.e., calculate value for char as it comes);
	This allows us to NOT spend extra time for constructing big_string;
	   */
	int n = s.size(), m = t.size();
	vector<int> pi_array = get_pi_array(s);
	vector<int> ans;
	int temp = 0;  // instead of appending a unique token to s with pi_array[n] = 0;
	// the below is an equivalent version of get_pi_array
	// apart from the if (temp == n) clause which is added here;
	for (int i=0; i<m; i++){
		if (t[i] == s[temp])
			temp++;
		else{
			while (temp > 0 && t[i] != s[temp])
				temp = pi_array[temp-1];
			if (temp > 0)
				temp++;
			else if (t[i] != s[temp])
				temp = 0;
			else
				temp = 1;
		}
		if (temp == n){
			ans.push_back(i-n+1);
			// when you find s in t, then for the next occurance
			// you must start at the longest prefix also a suffix of s;
			// e.g., "bobo" should be found twice in "bobobo";
			temp = pi_array[n-1]; 
		}
	}
	return ans;
}


int main(){
	string s = "bobo";
	string t = "boabsbobobobalskjbobecdkjf";
	cout<<"looking for\n"<<"\""<<s<<"\""<<'\n'<<"in\n"<<"\""<<t<<"\""<<"\n\n";
	auto idxs = kmp(s, t);
	printf("the first string occurs in the second string at indexes:\n");
	for (auto &id: idxs){
		cout<<id<<", ";
		assert(t.substr(id, s.size()) == s);
	}
	cout<<'\n';
	return 0;
}
