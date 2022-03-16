create table CASES
(
    CASE_ID       integer not null
        constraint CASES_pk
            primary key autoincrement,
    CASE_PACK     text    not null,
    CASE_NAM      text    not null,
    CASE_ENABLE   integer default 1 not null,
    CLIENT_EMU_ID integer,
    CLIENT_RECV   text,
    CLIENT_SEND   text,
    CLIENT_CHECK  text,
    SERVER_EMU_ID integer,
    SERVER_SEND   text,
    SERVER_RECV   text,
    SERVER_CHECK  text
);

create table EMULATORS
(
    EMULATOR_ID     integer not null
        constraint EMULATORS_pk
            primary key autoincrement,
    EMULATOR_PACK   text    not null,
    EMULATOR_NAM    text    not null,
    EMULATOR_SET    text    not null,
    EMULATOR_ENABLE integer default 1 not null,
    EMULATOR_SEED   integer default 0 not null,
    LISTEN_HOST     text,
    LISTEN_PORT     integer default -1 not null,
    LISTEN_TYP      text,
    CONN_HOST       text,
    CONN_PORT       integer default -1 not null,
    CONN_TYP        text,
    ENCODER         text,
    DECODER         text,
    CHECKER         text,
    CREATOR         text
);

create table HISTORY
(
    EXEC_ID         integer not null
        constraint HISTORY_pk
            primary key autoincrement,
    EXEC_STATUS     integer default 0 not null,
    EXEC_TIME_START integer,
    EXEC_TIME_END   integer,
    EXEC_RESULT     double
);

create table RECORDS
(
    RECORD_ID       integer not null
        constraint RECORDS_pk
            primary key autoincrement,
    EXEC_ID         integer not null,
    CASE_ID         integer not null,
    EMULATORS_ID    integer not null,
    RECORD_SEND_REL text,
    RECORD_RECV_REL integer,
    RECORD_RESULT   text
);
