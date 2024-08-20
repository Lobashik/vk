box.cfg{}

box.schema.user.create('dima', {password = 'dima1'})
box.schema.user.grant('dima', 'super')

-- Оставляем консоль открытой для взаимодействия
require('console').start()