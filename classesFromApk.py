import commands
import os
import fnmatch
import matplotlib.pyplot as plt
import collections


abs_path_dir = os.getcwd()
read_jars_folder_name = abs_path_dir + "/apks/read_jars"
text_file_errors = open('all_errors', 'w')


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def covert_to_jar(name_apk):
    os.system(abs_path_dir + "/dex2jar/dex2jar.sh " +
              os.getcwd() + "/apks/" + name_apk)


def conver_to_read_jar(name_file, name_folder):
    full_dir_name = abs_path_dir + "/apks/" + name_file
    path = "java -jar " + abs_path_dir + "/projects/fernflower.jar " + \
        full_dir_name + " " + name_folder
    os.system(path)


def get_all_files_with_pattern(pattern, folder):
    files = []
    for f in os.listdir(folder):
        if fnmatch.fnmatch(f, pattern):
            files.append(f)
    return files


def convert_all_apk_to_jar():
    for f in get_all_files_with_pattern("*.apk", abs_path_dir + "/apks/"):
        covert_to_jar(f)


def convert_all_jar_to_read_jar():
    ensure_dir(read_jars_folder_name)
    print get_all_files_with_pattern("*.jar", abs_path_dir + "/apks/")
    for f in get_all_files_with_pattern("*.jar", abs_path_dir + "/apks/"):
        conver_to_read_jar(f, read_jars_folder_name)


def unpack_all_jars_to_projects():
    files = get_all_files_with_pattern("*.jar", read_jars_folder_name)
    for f in files:
        path = "unzip " + read_jars_folder_name + "/" + \
            f + " -d " + abs_path_dir + "/projects/" + f[:-4]
        os.system(path)


def global_convert_to_projects():
    convert_all_apk_to_jar()
    convert_all_jar_to_read_jar()
    unpack_all_jars_to_projects()
    analysis_all_projects()


def project_analysis(folder):
    path_to_pmd = abs_path_dir + "/pmd/bin/"
    command = path_to_pmd + "run.sh pmd -d " + folder + \
        " -f text -R rulesets/java/basic.xml,rulesets/java/android.xml -version 1.7 -language java"
    status, output = commands.getstatusoutput(command)
    text_file_errors.write(output)


def analysis_all_projects():
    dir_name_proj = abs_path_dir + "/projects/"
    for folder in os.listdir(dir_name_proj):
        project_analysis(dir_name_proj + folder)
    text_file_errors.close()


def get_end_words(x, i):
    answer = ""
    for i in xrange(int(i), len(x)):
        answer += x[int(i)] + " "
    return answer


def delete_small_values(d):
    b = {}
    for k, v in d.iteritems():
        if v > 2:
            b[k] = v
    return b


def get_str_dict(d):
    s = ""
    for k, v in d.iteritems():
        s += str(k) + " - " + str(v) + "\n"
    return s


def draw_graph(d):
    d = delete_small_values(d)
    d = collections.OrderedDict(sorted(d.items()))
    text_statistic = open("statistic.txt", "w")
    text_statistic.write(get_str_dict(d))
    text_statistic.close()
    plt.bar(range(len(d)), d.values(), align='center')
    plt.xticks(range(len(d)), d.keys())
    plt.show()


def get_all_errors():
    strings = open("all_errors", "r+")
    warnings = {}
    for string in strings.readlines():
        x = string.split()
        key = ""
        if len(x[1]) > 2:
            key = get_end_words(x, 1)
        else:
            key = get_end_words(x, 2)

        if key in warnings:
            warnings[key] += 1
        else:
            warnings[key] = 1
    # print warnings
    return warnings


def main():
    global_convert_to_projects()
    text_file_errors.close()
    draw_graph(get_all_errors())


if __name__ == '__main__':
    main()
