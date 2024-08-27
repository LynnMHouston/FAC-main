begin;

do
$$
begin
    DROP SCHEMA IF EXISTS api_v1_1_1 CASCADE;
    DROP SCHEMA IF EXISTS api_v1_1_1_functions CASCADE;

    if not exists (select schema_name from information_schema.schemata where schema_name = 'api_v1_1_1') then
        create schema api_v1_1_1;
        create schema api_v1_1_1_functions;
        
        grant usage on schema api_v1_1_1_functions to api_fac_gov;

        -- Grant access to tables and views
        alter default privileges
            in schema api_v1_1_1
            grant select
        -- this includes views
        on tables
        to api_fac_gov;

        -- Grant access to sequences, if we have them
        grant usage on schema api_v1_1_1 to api_fac_gov;
        grant select, usage on all sequences in schema api_v1_1_1 to api_fac_gov;
        alter default privileges
            in schema api_v1_1_1
            grant select, usage
        on sequences
        to api_fac_gov;
    end if;
end
$$
;

-- https://postgrest.org/en/stable/references/api/openapi.html
-- This is the title (version number) and description (text).
COMMENT ON SCHEMA api_v1_1_1 IS
$$v1.1.1

A RESTful API that serves data from the SF-SAC.$$;


commit;

notify pgrst,
       'reload schema';
