--This will be used by the postgrest API_V1_0_0-BETA

begin;

do
$$
begin
    DROP SCHEMA IF EXISTS api_v1_0_0 CASCADE; 

    if not exists (select schema_name from information_schema.schemata where schema_name = 'api_v1_0_0') then
        create schema api_v1_0_0;

        -- Grant access to tables and views
        alter default privileges
            in schema api_v1_0_0
            grant select
        -- this includes views
        on tables
        to api_fac_gov;

        -- Grant access to sequences, if we have them
        grant usage on schema api_v1_0_0 to api_fac_gov;
        grant select, usage on all sequences in schema api_v1_0_0 to api_fac_gov;
        alter default privileges
            in schema api_v1_0_0
            grant select, usage
        on sequences
        to api_fac_gov;
    end if;
end
$$
;

-- This is the description
COMMENT ON SCHEMA api_v1_0_0 IS
    'The FAC dissemation API version 1.0.0-beta.'
;

-- https://postgrest.org/en/stable/references/api/openapi.html
-- This is the title
COMMENT ON SCHEMA api_v1_0_0 IS
$$v1.0.0-beta

A RESTful API that serves data from the SF-SAC.$$;

commit;

notify pgrst,
       'reload schema';
