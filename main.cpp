#include "ImageDisplaceLib.h"
using namespace std;

void testing(){
    vector<double> star = {54.12015333986315, 12.65005233482232, 0.25993125876773404, 0.8111479866192958};
    vector<double> ray = {0, 0};
    pair<double, double> res;

    res = get_displace_of_ray_by_single_star(star, ray);

    cout << res.first << " " << metres_to_mks(res.second);


}


void get_path(int x, int y, string code){

    std::uniform_real_distribution<> urd(0, 10);


    vector<vector<double>> stars = get_stars_set("C:\\Projects\\Astro\\stars.txt", 3597437, false);
    vector<vector<double>> velocities (stars.size());
    vector<vector<double>> corona_velocities (stars.size());

    corona_velocities = get_random_3d_velocity(stars.size(), 200, 250);
    velocities = get_random_3d_velocity(stars.size(), 15, 25);
    for (long i = 0; i < stars.size(); i++) {
        if (stars[i][4] > 0) velocities[i][0] += 225000;
        if (stars[i][4] == 0) velocities[i] = corona_velocities[i];
    }

    pair<int, int> time_config = {100, 60};
    long long full_duration = sec_in_year * time_config.first;
    long long interval = sec_in_day * time_config.second;
    double interval_double = interval;

    string path_to_file;
    path_to_file = "C:\\Projects\\Astro\\data\\path" + code + ".txt";
    ofstream fout(path_to_file);




    pair<double, double> image;
    vector<double> ray = {x * pc, y * pc};
    fout << "Path for ray(in pc) " << ray[0] / pc << " " << ray[1] / pc << endl;
    fout << "Points calculated each " << time_config.second << " days for " << time_config.first << " years." << endl;

    for (long long time_passed = 0; time_passed < full_duration; time_passed += interval){
        cout << "Calculating day " << time_passed / interval * time_config.second << endl;
        image = get_full_displace(stars, ray);
        fout << metres_to_mks(image.first) << " " << metres_to_mks(image.second) << endl;

        for (long i = 0; i < stars.size(); i++) for (int j = 0; j < 3; j++) {
                stars[i][j] += (velocities[i][j] * interval_double) / pc;
            }
    }


    fout.close();
}

void get_lattice_shift(int dist_btw_rays, vector<vector<double>> &stars){
    string dirname = "C:\\Projects\\Astro\\data\\shift\\shift_20x20_";
    ofstream fout(dirname + to_string(dist_btw_rays) + "mks");
    vector<double> ray = {0, 0};
    double step = mks_to_metres(dist_btw_rays);
    pair<double, double> displacement;
    cout << "working on distance " << dist_btw_rays << " mks" << endl;

    for (int i = 0; i < 20; i++){
        for (int j = 0; j < 20; j++){
            ray = {i * step, j * step};
            displacement = get_full_displace(stars, ray);
            fout << metres_to_mks(displacement.first) << " " << metres_to_mks(displacement.second) << endl;
            cout << "Ray " << i << " " << j << " counted" << endl;
        }
    }

    fout.close();
}

int main(){




    vector<vector<double>> stars = get_stars_set("C:\\Projects\\Astro\\stars.txt", 32607146, false);
    cout << "Stars are loaded" << endl;


    get_lattice_shift(5,stars);
    get_lattice_shift(10,stars);


    for (int i = 1; i < 7; i = i++){
        for (int j = 0; j < 10; j++){
        get_lattice_shift(pow(10, i) + pow(10, i - 1) * j,stars);
    }}

    cerr << "В непосредственной близости от звезды прошло лучей: " << close_stars_counter;

    return 0;
}

