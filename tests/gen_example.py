from rebasic import Engine

e = Engine()

with e.context.work_with_point('1') as ctx: # set current work point as 1
    ctx._add_tabs(1) # control tabs
    ctx.add_to_code(['test line 1', 'test line 2']) # add lines

with e.context.work_with_point('2') as ctx: 
    ctx._sub_tabs(1)
    ctx.add_to_code(['test line 3', 'test line 4']) 

with e.context.work_with_point('3') as ctx:
    ctx._add_tabs(2)
    ctx.add_to_code(['test line 5', 'test line 6'])

e.context.pipeline.set(['2', '1', '3']) # change pipeline
print(e.context.generate_code()) # generate code
''' ->
test line 3
test line 4

    test line 1
    test line 2

        test line 5
        test line 6
'''