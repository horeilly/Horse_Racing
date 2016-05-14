#!/bin/bash

rm PG.sql

cat stage1.sql >> PG.sql
seq 1 20 | xargs -Inone cat stage2.sql >> PG.sql
cat stage3.sql >> PG.sql

hive -f PG.sql >> errors.log

echo 'done'
