select e.employeeid,
        e.name_first,
        e.name_middle,
        e.name_last,
        e.name_initials,
        e.sex,
        e.language,
        e.phonenumber,
        e.emailaddress,
        e.loginname,
        a.*
from {{ ref('star_employees') }} e
join {{ ref('star_addresses') }} a
    on e.addressid = a.addressid