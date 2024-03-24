import { OrgIdToOrgMemberInfo } from "./org";
export type AccessHelper = {
    isRole: (orgId: string, role: string) => boolean;
    isAtLeastRole: (orgId: string, role: string) => boolean;
    hasPermission: (orgId: string, permission: string) => boolean;
    hasAllPermissions: (orgId: string, permissions: string[]) => boolean;
    getAccessHelperWithOrgId: (orgId: string) => AccessHelperWithOrg;
};
export type AccessHelperWithOrg = {
    isRole: (role: string) => boolean;
    isAtLeastRole: (role: string) => boolean;
    hasPermission: (permission: string) => boolean;
    hasAllPermissions: (permissions: string[]) => boolean;
};
export declare function getAccessHelper(orgIdToOrgMemberInfo: OrgIdToOrgMemberInfo): AccessHelper;
