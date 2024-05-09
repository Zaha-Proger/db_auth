from subprocess import run, STDOUT, PIPE
import textwrap
cmd = "last"

# перенаправляем `stdout` и `stderr` в переменную `output`
output = run(cmd.split(), stdout=PIPE, stderr=STDOUT, text=True)

        #записывается в список разделенная строка с разделителем \n
list = output.stdout.split("\n")
print(type(list))
# print(list[0])
# print(list[0][:9])
# print(list[0][9:22])
# print(list[0][22:39])
# print(list[0][39:42])
# print(list[0][43:50])
# print(list[0][50:56])
# print(list[0][58:63])
# print(list[0][64:])

print()

result = []
for i in range(len(list)-3):
#     text = textwrap.dedent(list[i][list[i].find(':', 15)+2:]).strip()
    
    result.append((
                        list[i][:9], 
                        list[i][9:22],
                        list[i][22:39],
                        list[i][39:42],
                        list[i][43:50],
                        list[i][50:63],
                        list[i][64:]
            ))
for r in result:
        print(r)