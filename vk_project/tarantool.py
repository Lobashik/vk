import tarantool


TARANTOOL_HOST = 'tarantool'
TARANTOOL_PORT = 3301
TARANTOOL_USER = 'dima'
TARANTOOL_PASSWORD = 'dima1'

connection = tarantool.Connection(
    host=TARANTOOL_HOST,
    port=TARANTOOL_PORT,
    user=TARANTOOL_USER,
    password=TARANTOOL_PASSWORD
    )


def create_user_space():
    connection.eval('''
    if box.sequence.user_id_seq == nil then
        box.schema.sequence.create('user_id_seq', {min = 1, start = 1})
    end
    if box.space.user == nil then
        local user = box.schema.space.create('user', {
        format = {
                {name = 'id', type = 'unsigned'},
                {name = 'username', type = 'string'},
                {name = 'email', type = 'string'},
                {name = 'password', type = 'string'}
            }
        })
        user:create_index('id', {
            parts = {'id'},
            sequence = 'user_id_seq',
            if_not_exists = true
        })
        user:create_index('username', {
            parts = {'username'},
            unique = true,
            if_not_exists = true
        })
    end
    '''
    )
    

def create_book_space():
    connection.eval('''
    if box.sequence.book_id_seq == nil then
        box.schema.sequence.create('book_id_seq', {min = 1, start = 1})
    end
    if box.space.book == nil then
        local book = box.schema.space.create('book', {
        format = {
                {name = 'id', type = 'unsigned'},
                {name = 'title', type = 'string'},
                {name = 'author', type = 'string'},
                {name = 'year', type = 'unsigned'}
            }
        })
        book:create_index('id', {
            parts = {'id'},
            sequence = 'user_id_seq',
            if_not_exists = true
        })
        book:create_index('title', {
            parts = {'title'},
            if_not_exists = true
        })
    end
    '''
    )


def read_by_titles():
    connection.eval('''
        function batch_read_by_title(titles)
        if titles == nil then
            error("No titles provided")
        end
        local results = {}
        for _, title in ipairs(titles) do
            local result = box.space.book.index.title:select(title)
            if result and #result > 0 then
                results[title] = result[1]
            end
        end
        return results
    end
    '''
    )


create_user_space()
create_book_space()
read_by_titles()
