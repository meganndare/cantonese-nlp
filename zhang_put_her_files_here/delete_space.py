import argparse
def delete_space(in_f,ou_f):
    f = open(in_f,encoding = "utf-8").read()
    sen = f.split("\n")
    output_lines = list()
    for line in sen:
        newline = line.replace(" ","")
        output_lines.append(newline)
        
    with open(ou_f, "a") as output_file:
        for line in output_lines:
            output_file.write(str(line+"\n"))
    output_file.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='I am too lazy to add a description here. You wrote the code. You know what\'s it for')
    parser.add_argument('--i', help='input path')
    parser.add_argument('--o', help='output path')
    args = parser.parse_args()
    delete_space(args.i,args.o)
