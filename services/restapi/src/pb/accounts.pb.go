// Code generated by protoc-gen-go. DO NOT EDIT.
// source: accounts.proto

package stabox

import (
	context "context"
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
	_ "google.golang.org/genproto/googleapis/api/annotations"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
	math "math"
)

// Reference imports to suppress errors if they are not otherwise used.
var _ = proto.Marshal
var _ = fmt.Errorf
var _ = math.Inf

// This is a compile-time assertion to ensure that this generated file
// is compatible with the proto package it is being compiled against.
// A compilation error at this line likely means your copy of the
// proto package needs to be updated.
const _ = proto.ProtoPackageIsVersion3 // please upgrade the proto package

type Account struct {
	XId string `protobuf:"bytes,1,opt,name=_id,json=Id,proto3" json:"_id,omitempty"`
	// Types that are valid to be assigned to Enabled_:
	//	*Account_Enabled
	Enabled_     isAccount_Enabled_ `protobuf_oneof:"enabled_"`
	Login        uint32             `protobuf:"varint,3,opt,name=login,proto3" json:"login,omitempty"`
	Password     string             `protobuf:"bytes,4,opt,name=password,proto3" json:"password,omitempty"`
	UserId       uint32             `protobuf:"varint,5,opt,name=user_id,json=userId,proto3" json:"user_id,omitempty"`
	AccountId    uint32             `protobuf:"varint,6,opt,name=account_id,json=accountId,proto3" json:"account_id,omitempty"`
	Rating       uint32             `protobuf:"varint,7,opt,name=rating,proto3" json:"rating,omitempty"`
	TzOffset     int32              `protobuf:"varint,8,opt,name=tz_offset,json=tzOffset,proto3" json:"tz_offset,omitempty"`
	ChannelId    uint32             `protobuf:"varint,9,opt,name=channel_id,json=channelId,proto3" json:"channel_id,omitempty"`
	VolumeLevel  uint32             `protobuf:"varint,10,opt,name=volume_level,json=volumeLevel,proto3" json:"volume_level,omitempty"`
	ParentCode   string             `protobuf:"bytes,11,opt,name=parent_code,json=parentCode,proto3" json:"parent_code,omitempty"`
	MaxStreams   uint32             `protobuf:"varint,12,opt,name=max_streams,json=maxStreams,proto3" json:"max_streams,omitempty"`
	MaxAddresses uint32             `protobuf:"varint,13,opt,name=max_addresses,json=maxAddresses,proto3" json:"max_addresses,omitempty"`
	// Types that are valid to be assigned to Autocolo_:
	//	*Account_Autocolo
	Autocolo_ isAccount_Autocolo_            `protobuf_oneof:"autocolo_"`
	LiveColo  *Colo                          `protobuf:"bytes,15,opt,name=live_colo,json=liveColo,proto3" json:"live_colo,omitempty"`
	DvrColo   *Colo                          `protobuf:"bytes,16,opt,name=dvr_colo,json=dvrColo,proto3" json:"dvr_colo,omitempty"`
	Abuses    map[string]*Account_ColoAbuses `protobuf:"bytes,17,rep,name=abuses,proto3" json:"abuses,omitempty" protobuf_key:"bytes,1,opt,name=key,proto3" protobuf_val:"bytes,2,opt,name=value,proto3"`
	IpAddress string                         `protobuf:"bytes,18,opt,name=ip_address,json=ipAddress,proto3" json:"ip_address,omitempty"`
	Location  *GeoLocation                   `protobuf:"bytes,19,opt,name=location,proto3" json:"location,omitempty"`
	// Types that are valid to be assigned to Trusted_:
	//	*Account_Trusted
	Trusted_             isAccount_Trusted_ `protobuf_oneof:"trusted_"`
	XXX_NoUnkeyedLiteral struct{}           `json:"-"`
	XXX_unrecognized     []byte             `json:"-"`
	XXX_sizecache        int32              `json:"-"`
}

func (m *Account) Reset()         { *m = Account{} }
func (m *Account) String() string { return proto.CompactTextString(m) }
func (*Account) ProtoMessage()    {}
func (*Account) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{0}
}

func (m *Account) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Account.Unmarshal(m, b)
}
func (m *Account) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Account.Marshal(b, m, deterministic)
}
func (m *Account) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Account.Merge(m, src)
}
func (m *Account) XXX_Size() int {
	return xxx_messageInfo_Account.Size(m)
}
func (m *Account) XXX_DiscardUnknown() {
	xxx_messageInfo_Account.DiscardUnknown(m)
}

var xxx_messageInfo_Account proto.InternalMessageInfo

func (m *Account) GetXId() string {
	if m != nil {
		return m.XId
	}
	return ""
}

type isAccount_Enabled_ interface {
	isAccount_Enabled_()
}

type Account_Enabled struct {
	Enabled bool `protobuf:"varint,2,opt,name=enabled,proto3,oneof"`
}

func (*Account_Enabled) isAccount_Enabled_() {}

func (m *Account) GetEnabled_() isAccount_Enabled_ {
	if m != nil {
		return m.Enabled_
	}
	return nil
}

func (m *Account) GetEnabled() bool {
	if x, ok := m.GetEnabled_().(*Account_Enabled); ok {
		return x.Enabled
	}
	return false
}

func (m *Account) GetLogin() uint32 {
	if m != nil {
		return m.Login
	}
	return 0
}

func (m *Account) GetPassword() string {
	if m != nil {
		return m.Password
	}
	return ""
}

func (m *Account) GetUserId() uint32 {
	if m != nil {
		return m.UserId
	}
	return 0
}

func (m *Account) GetAccountId() uint32 {
	if m != nil {
		return m.AccountId
	}
	return 0
}

func (m *Account) GetRating() uint32 {
	if m != nil {
		return m.Rating
	}
	return 0
}

func (m *Account) GetTzOffset() int32 {
	if m != nil {
		return m.TzOffset
	}
	return 0
}

func (m *Account) GetChannelId() uint32 {
	if m != nil {
		return m.ChannelId
	}
	return 0
}

func (m *Account) GetVolumeLevel() uint32 {
	if m != nil {
		return m.VolumeLevel
	}
	return 0
}

func (m *Account) GetParentCode() string {
	if m != nil {
		return m.ParentCode
	}
	return ""
}

func (m *Account) GetMaxStreams() uint32 {
	if m != nil {
		return m.MaxStreams
	}
	return 0
}

func (m *Account) GetMaxAddresses() uint32 {
	if m != nil {
		return m.MaxAddresses
	}
	return 0
}

type isAccount_Autocolo_ interface {
	isAccount_Autocolo_()
}

type Account_Autocolo struct {
	Autocolo bool `protobuf:"varint,14,opt,name=autocolo,proto3,oneof"`
}

func (*Account_Autocolo) isAccount_Autocolo_() {}

func (m *Account) GetAutocolo_() isAccount_Autocolo_ {
	if m != nil {
		return m.Autocolo_
	}
	return nil
}

func (m *Account) GetAutocolo() bool {
	if x, ok := m.GetAutocolo_().(*Account_Autocolo); ok {
		return x.Autocolo
	}
	return false
}

func (m *Account) GetLiveColo() *Colo {
	if m != nil {
		return m.LiveColo
	}
	return nil
}

func (m *Account) GetDvrColo() *Colo {
	if m != nil {
		return m.DvrColo
	}
	return nil
}

func (m *Account) GetAbuses() map[string]*Account_ColoAbuses {
	if m != nil {
		return m.Abuses
	}
	return nil
}

func (m *Account) GetIpAddress() string {
	if m != nil {
		return m.IpAddress
	}
	return ""
}

func (m *Account) GetLocation() *GeoLocation {
	if m != nil {
		return m.Location
	}
	return nil
}

type isAccount_Trusted_ interface {
	isAccount_Trusted_()
}

type Account_Trusted struct {
	Trusted bool `protobuf:"varint,20,opt,name=trusted,proto3,oneof"`
}

func (*Account_Trusted) isAccount_Trusted_() {}

func (m *Account) GetTrusted_() isAccount_Trusted_ {
	if m != nil {
		return m.Trusted_
	}
	return nil
}

func (m *Account) GetTrusted() bool {
	if x, ok := m.GetTrusted_().(*Account_Trusted); ok {
		return x.Trusted
	}
	return false
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*Account) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*Account_Enabled)(nil),
		(*Account_Autocolo)(nil),
		(*Account_Trusted)(nil),
	}
}

type Account_ColoAbuses struct {
	Timestamps           []uint32 `protobuf:"varint,1,rep,packed,name=timestamps,proto3" json:"timestamps,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *Account_ColoAbuses) Reset()         { *m = Account_ColoAbuses{} }
func (m *Account_ColoAbuses) String() string { return proto.CompactTextString(m) }
func (*Account_ColoAbuses) ProtoMessage()    {}
func (*Account_ColoAbuses) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{0, 0}
}

func (m *Account_ColoAbuses) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_Account_ColoAbuses.Unmarshal(m, b)
}
func (m *Account_ColoAbuses) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_Account_ColoAbuses.Marshal(b, m, deterministic)
}
func (m *Account_ColoAbuses) XXX_Merge(src proto.Message) {
	xxx_messageInfo_Account_ColoAbuses.Merge(m, src)
}
func (m *Account_ColoAbuses) XXX_Size() int {
	return xxx_messageInfo_Account_ColoAbuses.Size(m)
}
func (m *Account_ColoAbuses) XXX_DiscardUnknown() {
	xxx_messageInfo_Account_ColoAbuses.DiscardUnknown(m)
}

var xxx_messageInfo_Account_ColoAbuses proto.InternalMessageInfo

func (m *Account_ColoAbuses) GetTimestamps() []uint32 {
	if m != nil {
		return m.Timestamps
	}
	return nil
}

type GetAccountsReq struct {
	Skip                 uint32   `protobuf:"varint,2,opt,name=skip,proto3" json:"skip,omitempty"`
	Limit                uint32   `protobuf:"varint,3,opt,name=limit,proto3" json:"limit,omitempty"`
	Fields               string   `protobuf:"bytes,5,opt,name=fields,proto3" json:"fields,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *GetAccountsReq) Reset()         { *m = GetAccountsReq{} }
func (m *GetAccountsReq) String() string { return proto.CompactTextString(m) }
func (*GetAccountsReq) ProtoMessage()    {}
func (*GetAccountsReq) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{1}
}

func (m *GetAccountsReq) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetAccountsReq.Unmarshal(m, b)
}
func (m *GetAccountsReq) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetAccountsReq.Marshal(b, m, deterministic)
}
func (m *GetAccountsReq) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetAccountsReq.Merge(m, src)
}
func (m *GetAccountsReq) XXX_Size() int {
	return xxx_messageInfo_GetAccountsReq.Size(m)
}
func (m *GetAccountsReq) XXX_DiscardUnknown() {
	xxx_messageInfo_GetAccountsReq.DiscardUnknown(m)
}

var xxx_messageInfo_GetAccountsReq proto.InternalMessageInfo

func (m *GetAccountsReq) GetSkip() uint32 {
	if m != nil {
		return m.Skip
	}
	return 0
}

func (m *GetAccountsReq) GetLimit() uint32 {
	if m != nil {
		return m.Limit
	}
	return 0
}

func (m *GetAccountsReq) GetFields() string {
	if m != nil {
		return m.Fields
	}
	return ""
}

type GetAccountsRep struct {
	Accounts             []*Account `protobuf:"bytes,1,rep,name=accounts,proto3" json:"accounts,omitempty"`
	Offset               uint32     `protobuf:"varint,2,opt,name=offset,proto3" json:"offset,omitempty"`
	Count                uint32     `protobuf:"varint,3,opt,name=count,proto3" json:"count,omitempty"`
	Total                uint32     `protobuf:"varint,4,opt,name=total,proto3" json:"total,omitempty"`
	XXX_NoUnkeyedLiteral struct{}   `json:"-"`
	XXX_unrecognized     []byte     `json:"-"`
	XXX_sizecache        int32      `json:"-"`
}

func (m *GetAccountsRep) Reset()         { *m = GetAccountsRep{} }
func (m *GetAccountsRep) String() string { return proto.CompactTextString(m) }
func (*GetAccountsRep) ProtoMessage()    {}
func (*GetAccountsRep) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{2}
}

func (m *GetAccountsRep) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_GetAccountsRep.Unmarshal(m, b)
}
func (m *GetAccountsRep) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_GetAccountsRep.Marshal(b, m, deterministic)
}
func (m *GetAccountsRep) XXX_Merge(src proto.Message) {
	xxx_messageInfo_GetAccountsRep.Merge(m, src)
}
func (m *GetAccountsRep) XXX_Size() int {
	return xxx_messageInfo_GetAccountsRep.Size(m)
}
func (m *GetAccountsRep) XXX_DiscardUnknown() {
	xxx_messageInfo_GetAccountsRep.DiscardUnknown(m)
}

var xxx_messageInfo_GetAccountsRep proto.InternalMessageInfo

func (m *GetAccountsRep) GetAccounts() []*Account {
	if m != nil {
		return m.Accounts
	}
	return nil
}

func (m *GetAccountsRep) GetOffset() uint32 {
	if m != nil {
		return m.Offset
	}
	return 0
}

func (m *GetAccountsRep) GetCount() uint32 {
	if m != nil {
		return m.Count
	}
	return 0
}

func (m *GetAccountsRep) GetTotal() uint32 {
	if m != nil {
		return m.Total
	}
	return 0
}

type UpdateAccountsReq struct {
	Query                *Account `protobuf:"bytes,1,opt,name=query,proto3" json:"query,omitempty"`
	Set                  *Account `protobuf:"bytes,2,opt,name=set,proto3" json:"set,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *UpdateAccountsReq) Reset()         { *m = UpdateAccountsReq{} }
func (m *UpdateAccountsReq) String() string { return proto.CompactTextString(m) }
func (*UpdateAccountsReq) ProtoMessage()    {}
func (*UpdateAccountsReq) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{3}
}

func (m *UpdateAccountsReq) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_UpdateAccountsReq.Unmarshal(m, b)
}
func (m *UpdateAccountsReq) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_UpdateAccountsReq.Marshal(b, m, deterministic)
}
func (m *UpdateAccountsReq) XXX_Merge(src proto.Message) {
	xxx_messageInfo_UpdateAccountsReq.Merge(m, src)
}
func (m *UpdateAccountsReq) XXX_Size() int {
	return xxx_messageInfo_UpdateAccountsReq.Size(m)
}
func (m *UpdateAccountsReq) XXX_DiscardUnknown() {
	xxx_messageInfo_UpdateAccountsReq.DiscardUnknown(m)
}

var xxx_messageInfo_UpdateAccountsReq proto.InternalMessageInfo

func (m *UpdateAccountsReq) GetQuery() *Account {
	if m != nil {
		return m.Query
	}
	return nil
}

func (m *UpdateAccountsReq) GetSet() *Account {
	if m != nil {
		return m.Set
	}
	return nil
}

type UpdateAccountsRep struct {
	Affected             uint32   `protobuf:"varint,1,opt,name=affected,proto3" json:"affected,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *UpdateAccountsRep) Reset()         { *m = UpdateAccountsRep{} }
func (m *UpdateAccountsRep) String() string { return proto.CompactTextString(m) }
func (*UpdateAccountsRep) ProtoMessage()    {}
func (*UpdateAccountsRep) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{4}
}

func (m *UpdateAccountsRep) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_UpdateAccountsRep.Unmarshal(m, b)
}
func (m *UpdateAccountsRep) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_UpdateAccountsRep.Marshal(b, m, deterministic)
}
func (m *UpdateAccountsRep) XXX_Merge(src proto.Message) {
	xxx_messageInfo_UpdateAccountsRep.Merge(m, src)
}
func (m *UpdateAccountsRep) XXX_Size() int {
	return xxx_messageInfo_UpdateAccountsRep.Size(m)
}
func (m *UpdateAccountsRep) XXX_DiscardUnknown() {
	xxx_messageInfo_UpdateAccountsRep.DiscardUnknown(m)
}

var xxx_messageInfo_UpdateAccountsRep proto.InternalMessageInfo

func (m *UpdateAccountsRep) GetAffected() uint32 {
	if m != nil {
		return m.Affected
	}
	return 0
}

type SessionCreateReq struct {
	Login                uint32   `protobuf:"varint,1,opt,name=login,proto3" json:"login,omitempty"`
	Password             string   `protobuf:"bytes,2,opt,name=password,proto3" json:"password,omitempty"`
	UserAgent            string   `protobuf:"bytes,3,opt,name=user_agent,json=userAgent,proto3" json:"user_agent,omitempty"`
	IpAddress            string   `protobuf:"bytes,4,opt,name=ip_address,json=ipAddress,proto3" json:"ip_address,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *SessionCreateReq) Reset()         { *m = SessionCreateReq{} }
func (m *SessionCreateReq) String() string { return proto.CompactTextString(m) }
func (*SessionCreateReq) ProtoMessage()    {}
func (*SessionCreateReq) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{5}
}

func (m *SessionCreateReq) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_SessionCreateReq.Unmarshal(m, b)
}
func (m *SessionCreateReq) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_SessionCreateReq.Marshal(b, m, deterministic)
}
func (m *SessionCreateReq) XXX_Merge(src proto.Message) {
	xxx_messageInfo_SessionCreateReq.Merge(m, src)
}
func (m *SessionCreateReq) XXX_Size() int {
	return xxx_messageInfo_SessionCreateReq.Size(m)
}
func (m *SessionCreateReq) XXX_DiscardUnknown() {
	xxx_messageInfo_SessionCreateReq.DiscardUnknown(m)
}

var xxx_messageInfo_SessionCreateReq proto.InternalMessageInfo

func (m *SessionCreateReq) GetLogin() uint32 {
	if m != nil {
		return m.Login
	}
	return 0
}

func (m *SessionCreateReq) GetPassword() string {
	if m != nil {
		return m.Password
	}
	return ""
}

func (m *SessionCreateReq) GetUserAgent() string {
	if m != nil {
		return m.UserAgent
	}
	return ""
}

func (m *SessionCreateReq) GetIpAddress() string {
	if m != nil {
		return m.IpAddress
	}
	return ""
}

type AccountSession struct {
	XId       string `protobuf:"bytes,1,opt,name=_id,json=Id,proto3" json:"_id,omitempty"`
	Login     uint32 `protobuf:"varint,2,opt,name=login,proto3" json:"login,omitempty"`
	UserAgent string `protobuf:"bytes,3,opt,name=user_agent,json=userAgent,proto3" json:"user_agent,omitempty"`
	IpAddress string `protobuf:"bytes,4,opt,name=ip_address,json=ipAddress,proto3" json:"ip_address,omitempty"`
	CreatedAt string `protobuf:"bytes,5,opt,name=created_at,json=createdAt,proto3" json:"created_at,omitempty"`
	// Types that are valid to be assigned to Active_:
	//	*AccountSession_Active
	Active_              isAccountSession_Active_ `protobuf_oneof:"active_"`
	Location             *GeoLocation             `protobuf:"bytes,7,opt,name=location,proto3" json:"location,omitempty"`
	XXX_NoUnkeyedLiteral struct{}                 `json:"-"`
	XXX_unrecognized     []byte                   `json:"-"`
	XXX_sizecache        int32                    `json:"-"`
}

func (m *AccountSession) Reset()         { *m = AccountSession{} }
func (m *AccountSession) String() string { return proto.CompactTextString(m) }
func (*AccountSession) ProtoMessage()    {}
func (*AccountSession) Descriptor() ([]byte, []int) {
	return fileDescriptor_e1e7723af4c007b7, []int{6}
}

func (m *AccountSession) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_AccountSession.Unmarshal(m, b)
}
func (m *AccountSession) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_AccountSession.Marshal(b, m, deterministic)
}
func (m *AccountSession) XXX_Merge(src proto.Message) {
	xxx_messageInfo_AccountSession.Merge(m, src)
}
func (m *AccountSession) XXX_Size() int {
	return xxx_messageInfo_AccountSession.Size(m)
}
func (m *AccountSession) XXX_DiscardUnknown() {
	xxx_messageInfo_AccountSession.DiscardUnknown(m)
}

var xxx_messageInfo_AccountSession proto.InternalMessageInfo

func (m *AccountSession) GetXId() string {
	if m != nil {
		return m.XId
	}
	return ""
}

func (m *AccountSession) GetLogin() uint32 {
	if m != nil {
		return m.Login
	}
	return 0
}

func (m *AccountSession) GetUserAgent() string {
	if m != nil {
		return m.UserAgent
	}
	return ""
}

func (m *AccountSession) GetIpAddress() string {
	if m != nil {
		return m.IpAddress
	}
	return ""
}

func (m *AccountSession) GetCreatedAt() string {
	if m != nil {
		return m.CreatedAt
	}
	return ""
}

type isAccountSession_Active_ interface {
	isAccountSession_Active_()
}

type AccountSession_Active struct {
	Active bool `protobuf:"varint,6,opt,name=active,proto3,oneof"`
}

func (*AccountSession_Active) isAccountSession_Active_() {}

func (m *AccountSession) GetActive_() isAccountSession_Active_ {
	if m != nil {
		return m.Active_
	}
	return nil
}

func (m *AccountSession) GetActive() bool {
	if x, ok := m.GetActive_().(*AccountSession_Active); ok {
		return x.Active
	}
	return false
}

func (m *AccountSession) GetLocation() *GeoLocation {
	if m != nil {
		return m.Location
	}
	return nil
}

// XXX_OneofWrappers is for the internal use of the proto package.
func (*AccountSession) XXX_OneofWrappers() []interface{} {
	return []interface{}{
		(*AccountSession_Active)(nil),
	}
}

func init() {
	proto.RegisterType((*Account)(nil), "stabox.Account")
	proto.RegisterMapType((map[string]*Account_ColoAbuses)(nil), "stabox.Account.AbusesEntry")
	proto.RegisterType((*Account_ColoAbuses)(nil), "stabox.Account.ColoAbuses")
	proto.RegisterType((*GetAccountsReq)(nil), "stabox.GetAccountsReq")
	proto.RegisterType((*GetAccountsRep)(nil), "stabox.GetAccountsRep")
	proto.RegisterType((*UpdateAccountsReq)(nil), "stabox.updateAccountsReq")
	proto.RegisterType((*UpdateAccountsRep)(nil), "stabox.updateAccountsRep")
	proto.RegisterType((*SessionCreateReq)(nil), "stabox.SessionCreateReq")
	proto.RegisterType((*AccountSession)(nil), "stabox.AccountSession")
}

func init() { proto.RegisterFile("accounts.proto", fileDescriptor_e1e7723af4c007b7) }

var fileDescriptor_e1e7723af4c007b7 = []byte{
	// 922 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xa4, 0x55, 0xcd, 0x6e, 0xdb, 0x46,
	0x10, 0x2e, 0x25, 0x4b, 0x22, 0x87, 0x96, 0x6c, 0xad, 0x0d, 0x97, 0x65, 0x9c, 0x46, 0x61, 0x11,
	0x54, 0x4d, 0x0b, 0xab, 0x50, 0x2e, 0x85, 0x6f, 0xb2, 0x51, 0xa4, 0x02, 0x02, 0xa4, 0x60, 0xd0,
	0x63, 0x41, 0xac, 0xc5, 0x91, 0x42, 0x84, 0xe2, 0x32, 0xdc, 0x15, 0xeb, 0xa4, 0xe8, 0xa1, 0x79,
	0x85, 0x3e, 0x4e, 0x1f, 0xa3, 0x6f, 0x50, 0xf4, 0xd4, 0xa7, 0x28, 0xf6, 0x87, 0x94, 0x4c, 0xbb,
	0x80, 0x81, 0xdc, 0x34, 0xdf, 0x7c, 0xfb, 0xed, 0xcc, 0xf2, 0x9b, 0x11, 0x0c, 0xe8, 0x62, 0xc1,
	0x36, 0x99, 0xe0, 0x67, 0x79, 0xc1, 0x04, 0x23, 0x5d, 0x2e, 0xe8, 0x15, 0xbb, 0xf6, 0x07, 0x1c,
	0x8b, 0x32, 0x59, 0xa0, 0xc1, 0xfd, 0xe1, 0x0a, 0x59, 0x81, 0x9c, 0xa5, 0x25, 0x16, 0x06, 0x3a,
	0x5d, 0x31, 0xb6, 0x4a, 0x71, 0x42, 0xf3, 0x64, 0x42, 0xb3, 0x8c, 0x09, 0x2a, 0x12, 0x96, 0x99,
	0x03, 0xc1, 0x9f, 0x5d, 0xe8, 0xcd, 0xb4, 0x36, 0x39, 0x80, 0x76, 0x94, 0xc4, 0x9e, 0x35, 0xb2,
	0xc6, 0x4e, 0xd8, 0x9a, 0xc7, 0xc4, 0x87, 0x1e, 0x66, 0xf4, 0x2a, 0xc5, 0xd8, 0x6b, 0x8d, 0xac,
	0xb1, 0xfd, 0xc3, 0x27, 0x61, 0x05, 0x90, 0x63, 0xe8, 0xa4, 0x6c, 0x95, 0x64, 0x5e, 0x7b, 0x64,
	0x8d, 0xfb, 0xa1, 0x0e, 0x88, 0x0f, 0x76, 0x4e, 0x39, 0xff, 0x85, 0x15, 0xb1, 0xb7, 0xa7, 0x74,
	0xea, 0x98, 0x7c, 0x0a, 0xbd, 0x0d, 0xc7, 0x42, 0x5e, 0xd1, 0x51, 0x67, 0xba, 0x32, 0x9c, 0xc7,
	0xe4, 0x21, 0x80, 0x69, 0x4f, 0xe6, 0xba, 0x2a, 0xe7, 0x18, 0x64, 0x1e, 0x93, 0x13, 0xe8, 0x16,
	0x54, 0x24, 0xd9, 0xca, 0xeb, 0xe9, 0x63, 0x3a, 0x22, 0x0f, 0xc0, 0x11, 0xef, 0x23, 0xb6, 0x5c,
	0x72, 0x14, 0x9e, 0x3d, 0xb2, 0xc6, 0x9d, 0xd0, 0x16, 0xef, 0x5f, 0xaa, 0x58, 0x6a, 0x2e, 0x5e,
	0xd3, 0x2c, 0xc3, 0x54, 0x6a, 0x3a, 0x5a, 0xd3, 0x20, 0xf3, 0x98, 0x3c, 0x86, 0xfd, 0x92, 0xa5,
	0x9b, 0x35, 0x46, 0x29, 0x96, 0x98, 0x7a, 0xa0, 0x08, 0xae, 0xc6, 0x5e, 0x48, 0x88, 0x3c, 0x02,
	0x37, 0xa7, 0x05, 0x66, 0x22, 0x5a, 0xb0, 0x18, 0x3d, 0x57, 0x75, 0x03, 0x1a, 0xba, 0x64, 0x31,
	0x4a, 0xc2, 0x9a, 0x5e, 0x47, 0x5c, 0x14, 0x48, 0xd7, 0xdc, 0xdb, 0x57, 0x12, 0xb0, 0xa6, 0xd7,
	0xaf, 0x34, 0x42, 0xbe, 0x80, 0xbe, 0x24, 0xd0, 0x38, 0x2e, 0x90, 0x73, 0xe4, 0x5e, 0x5f, 0x51,
	0xf6, 0xd7, 0xf4, 0x7a, 0x56, 0x61, 0xe4, 0x14, 0x6c, 0xba, 0x11, 0x6c, 0xc1, 0x52, 0xe6, 0x0d,
	0xd4, 0x23, 0x5b, 0x61, 0x8d, 0x90, 0xaf, 0xc0, 0x49, 0x93, 0x12, 0x23, 0x95, 0x3e, 0x18, 0x59,
	0x63, 0x77, 0xba, 0x7f, 0xa6, 0xbf, 0xfd, 0xd9, 0x25, 0x4b, 0x59, 0x68, 0xcb, 0xb4, 0xfc, 0x45,
	0xbe, 0x04, 0x3b, 0x2e, 0x0b, 0xcd, 0x3c, 0xbc, 0x83, 0xd9, 0x8b, 0xcb, 0x42, 0x11, 0x9f, 0x41,
	0x97, 0x5e, 0x6d, 0x64, 0x3d, 0xc3, 0x51, 0x7b, 0xec, 0x4e, 0x1f, 0x54, 0x34, 0xe3, 0x83, 0xb3,
	0x99, 0xca, 0x7e, 0x9f, 0x89, 0xe2, 0x5d, 0x68, 0xa8, 0xf2, 0x3d, 0x93, 0xbc, 0x6a, 0xc5, 0x23,
	0xea, 0x31, 0x9c, 0x24, 0x37, 0x7d, 0x90, 0x09, 0xd8, 0x29, 0x5b, 0x28, 0x67, 0x79, 0x47, 0xea,
	0xf2, 0xa3, 0x4a, 0xf5, 0x39, 0xb2, 0x17, 0x26, 0x15, 0xd6, 0x24, 0x69, 0x2d, 0x51, 0x6c, 0xb8,
	0xc0, 0xd8, 0x3b, 0x56, 0x5d, 0xb7, 0xc2, 0x0a, 0xf0, 0xbf, 0x01, 0x90, 0x85, 0xea, 0x32, 0xc8,
	0xe7, 0x00, 0x22, 0x59, 0x23, 0x17, 0x74, 0x9d, 0x73, 0xcf, 0x1a, 0xb5, 0xe5, 0x2b, 0x6f, 0x11,
	0xff, 0x27, 0x70, 0x77, 0x0a, 0x26, 0x87, 0xd0, 0x7e, 0x83, 0xef, 0x8c, 0x89, 0xe5, 0x4f, 0xf2,
	0x2d, 0x74, 0x4a, 0x9a, 0x6e, 0x50, 0x79, 0xd8, 0x9d, 0xfa, 0xcd, 0x76, 0xb7, 0x77, 0x85, 0x9a,
	0x78, 0xde, 0xfa, 0xce, 0xba, 0x00, 0xb0, 0x8d, 0xd5, 0xa3, 0x0b, 0x17, 0x9c, 0xea, 0x8b, 0x44,
	0x32, 0x61, 0x0a, 0x8d, 0x82, 0x10, 0x06, 0xcf, 0x51, 0x18, 0x21, 0x1e, 0xe2, 0x5b, 0x42, 0x60,
	0x8f, 0xbf, 0x49, 0x72, 0x75, 0x57, 0x3f, 0x54, 0xbf, 0xd5, 0xa8, 0x24, 0xeb, 0x44, 0xd4, 0xa3,
	0x22, 0x03, 0x69, 0xeb, 0x65, 0x82, 0x69, 0xcc, 0xd5, 0x34, 0x38, 0xa1, 0x89, 0x82, 0xdf, 0xad,
	0x86, 0x68, 0x4e, 0xbe, 0x06, 0xbb, 0x9a, 0x7f, 0xf5, 0x00, 0xee, 0xf4, 0xa0, 0xd1, 0x44, 0x58,
	0x13, 0xa4, 0xae, 0x99, 0x09, 0x5d, 0x83, 0x89, 0x64, 0x15, 0x8a, 0x51, 0x55, 0xa1, 0x67, 0xfe,
	0x18, 0x3a, 0x82, 0x09, 0x9a, 0xaa, 0x69, 0xed, 0x87, 0x3a, 0x08, 0x7e, 0x86, 0xe1, 0x26, 0x8f,
	0xa9, 0xc0, 0xdd, 0xd6, 0x9e, 0x40, 0xe7, 0xed, 0x06, 0x0b, 0xfd, 0xb6, 0x77, 0x94, 0xa0, 0xb3,
	0xe4, 0x31, 0xb4, 0xab, 0xcb, 0xef, 0x20, 0xc9, 0x5c, 0x30, 0xb9, 0x2d, 0x9f, 0xcb, 0xd5, 0x41,
	0x97, 0x4b, 0x5c, 0x48, 0x4b, 0x58, 0xaa, 0x98, 0x3a, 0x0e, 0x3e, 0x58, 0x70, 0xf8, 0x0a, 0x39,
	0x4f, 0x58, 0x76, 0x59, 0x20, 0x15, 0x28, 0xeb, 0xa9, 0x37, 0x90, 0xf5, 0x7f, 0x1b, 0xa8, 0xd5,
	0xd8, 0x40, 0x0f, 0x01, 0xd4, 0x06, 0xa2, 0x2b, 0x34, 0xef, 0xe0, 0x84, 0x8e, 0x44, 0x66, 0x12,
	0x68, 0x78, 0x7c, 0xaf, 0xe1, 0xf1, 0xe0, 0x5f, 0x0b, 0x06, 0xa6, 0x60, 0x53, 0xcb, 0xed, 0x8d,
	0x59, 0xd7, 0xd4, 0xda, 0xad, 0xe9, 0xa3, 0xee, 0x55, 0xab, 0x4c, 0x35, 0x1d, 0x47, 0x54, 0x18,
	0xb3, 0x38, 0x06, 0x99, 0x09, 0xe2, 0x41, 0x97, 0x2e, 0x44, 0x52, 0xa2, 0xda, 0x9c, 0x72, 0x47,
	0x9b, 0xf8, 0xc6, 0x50, 0xf6, 0xee, 0x31, 0x94, 0x17, 0x0e, 0xf4, 0xf4, 0xd1, 0x68, 0xfa, 0x77,
	0x0b, 0xec, 0xea, 0xeb, 0x90, 0x1f, 0xc1, 0xdd, 0x71, 0x24, 0x39, 0xd9, 0xaa, 0xec, 0x7a, 0xdf,
	0xbf, 0x1b, 0xcf, 0x83, 0xe1, 0x87, 0xbf, 0xfe, 0xf9, 0xa3, 0xe5, 0x12, 0x67, 0x52, 0x9b, 0x74,
	0x0e, 0xb0, 0x25, 0x91, 0xa6, 0x4b, 0xfc, 0x26, 0x10, 0x7c, 0xa6, 0x24, 0x8e, 0xc8, 0xb0, 0x96,
	0x98, 0xfc, 0xaa, 0xde, 0xf6, 0x37, 0xf2, 0x12, 0xfa, 0x37, 0xcc, 0x74, 0x0f, 0xb5, 0x53, 0xa5,
	0x76, 0x32, 0xbd, 0xad, 0x76, 0x6e, 0x3d, 0x25, 0xaf, 0xa1, 0x7f, 0xc3, 0x6b, 0xc4, 0xab, 0xce,
	0x37, 0x2d, 0xb8, 0xed, 0xf8, 0xa6, 0x2f, 0x82, 0x27, 0xea, 0x82, 0x47, 0x81, 0x7f, 0xeb, 0x82,
	0x09, 0xd7, 0x14, 0x7e, 0x6e, 0x3d, 0xbd, 0xea, 0xaa, 0xff, 0xe0, 0x67, 0xff, 0x05, 0x00, 0x00,
	0xff, 0xff, 0xe6, 0x01, 0x95, 0x30, 0xde, 0x07, 0x00, 0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// AccountsClient is the client API for Accounts service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type AccountsClient interface {
	GetAccounts(ctx context.Context, in *GetAccountsReq, opts ...grpc.CallOption) (*GetAccountsRep, error)
	GetAccount(ctx context.Context, in *Account, opts ...grpc.CallOption) (*Account, error)
	UpdateAccount(ctx context.Context, in *Account, opts ...grpc.CallOption) (*Account, error)
	// rpc updateAccounts(updateAccountsReq) returns (Account) {
	//     option (google.api.http) = {
	//         patch: "/accounts/{login}",
	//         body: "*"
	//     };
	// }
	SessionCreate(ctx context.Context, in *SessionCreateReq, opts ...grpc.CallOption) (*AccountSession, error)
}

type accountsClient struct {
	cc *grpc.ClientConn
}

func NewAccountsClient(cc *grpc.ClientConn) AccountsClient {
	return &accountsClient{cc}
}

func (c *accountsClient) GetAccounts(ctx context.Context, in *GetAccountsReq, opts ...grpc.CallOption) (*GetAccountsRep, error) {
	out := new(GetAccountsRep)
	err := c.cc.Invoke(ctx, "/stabox.Accounts/GetAccounts", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *accountsClient) GetAccount(ctx context.Context, in *Account, opts ...grpc.CallOption) (*Account, error) {
	out := new(Account)
	err := c.cc.Invoke(ctx, "/stabox.Accounts/GetAccount", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *accountsClient) UpdateAccount(ctx context.Context, in *Account, opts ...grpc.CallOption) (*Account, error) {
	out := new(Account)
	err := c.cc.Invoke(ctx, "/stabox.Accounts/updateAccount", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *accountsClient) SessionCreate(ctx context.Context, in *SessionCreateReq, opts ...grpc.CallOption) (*AccountSession, error) {
	out := new(AccountSession)
	err := c.cc.Invoke(ctx, "/stabox.Accounts/SessionCreate", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// AccountsServer is the server API for Accounts service.
type AccountsServer interface {
	GetAccounts(context.Context, *GetAccountsReq) (*GetAccountsRep, error)
	GetAccount(context.Context, *Account) (*Account, error)
	UpdateAccount(context.Context, *Account) (*Account, error)
	// rpc updateAccounts(updateAccountsReq) returns (Account) {
	//     option (google.api.http) = {
	//         patch: "/accounts/{login}",
	//         body: "*"
	//     };
	// }
	SessionCreate(context.Context, *SessionCreateReq) (*AccountSession, error)
}

// UnimplementedAccountsServer can be embedded to have forward compatible implementations.
type UnimplementedAccountsServer struct {
}

func (*UnimplementedAccountsServer) GetAccounts(ctx context.Context, req *GetAccountsReq) (*GetAccountsRep, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetAccounts not implemented")
}
func (*UnimplementedAccountsServer) GetAccount(ctx context.Context, req *Account) (*Account, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetAccount not implemented")
}
func (*UnimplementedAccountsServer) UpdateAccount(ctx context.Context, req *Account) (*Account, error) {
	return nil, status.Errorf(codes.Unimplemented, "method UpdateAccount not implemented")
}
func (*UnimplementedAccountsServer) SessionCreate(ctx context.Context, req *SessionCreateReq) (*AccountSession, error) {
	return nil, status.Errorf(codes.Unimplemented, "method SessionCreate not implemented")
}

func RegisterAccountsServer(s *grpc.Server, srv AccountsServer) {
	s.RegisterService(&_Accounts_serviceDesc, srv)
}

func _Accounts_GetAccounts_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(GetAccountsReq)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AccountsServer).GetAccounts(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/stabox.Accounts/GetAccounts",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AccountsServer).GetAccounts(ctx, req.(*GetAccountsReq))
	}
	return interceptor(ctx, in, info, handler)
}

func _Accounts_GetAccount_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Account)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AccountsServer).GetAccount(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/stabox.Accounts/GetAccount",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AccountsServer).GetAccount(ctx, req.(*Account))
	}
	return interceptor(ctx, in, info, handler)
}

func _Accounts_UpdateAccount_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(Account)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AccountsServer).UpdateAccount(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/stabox.Accounts/UpdateAccount",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AccountsServer).UpdateAccount(ctx, req.(*Account))
	}
	return interceptor(ctx, in, info, handler)
}

func _Accounts_SessionCreate_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SessionCreateReq)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(AccountsServer).SessionCreate(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/stabox.Accounts/SessionCreate",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(AccountsServer).SessionCreate(ctx, req.(*SessionCreateReq))
	}
	return interceptor(ctx, in, info, handler)
}

var _Accounts_serviceDesc = grpc.ServiceDesc{
	ServiceName: "stabox.Accounts",
	HandlerType: (*AccountsServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "GetAccounts",
			Handler:    _Accounts_GetAccounts_Handler,
		},
		{
			MethodName: "GetAccount",
			Handler:    _Accounts_GetAccount_Handler,
		},
		{
			MethodName: "updateAccount",
			Handler:    _Accounts_UpdateAccount_Handler,
		},
		{
			MethodName: "SessionCreate",
			Handler:    _Accounts_SessionCreate_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "accounts.proto",
}