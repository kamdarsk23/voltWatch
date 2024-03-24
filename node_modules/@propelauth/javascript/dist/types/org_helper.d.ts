import { OrgIdToOrgMemberInfo, OrgMemberInfo } from "./org";
export type OrgHelper = {
    getOrgs: () => OrgMemberInfo[];
    getOrgIds: () => string[];
    getOrg: (orgId: string) => OrgMemberInfo | undefined;
    getOrgByName: (orgName: string) => OrgMemberInfo | undefined;
};
export declare function getOrgHelper(orgIdToOrgMemberInfo: OrgIdToOrgMemberInfo): OrgHelper;
