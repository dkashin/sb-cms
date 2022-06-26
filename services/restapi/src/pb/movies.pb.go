// Code generated by protoc-gen-go. DO NOT EDIT.
// source: movies.proto

package stabox

import (
	context "context"
	fmt "fmt"
	proto "github.com/golang/protobuf/proto"
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

type MovieFile struct {
	XId                  string   `protobuf:"bytes,1,opt,name=_id,json=Id,proto3" json:"_id,omitempty"`
	FileId               uint32   `protobuf:"varint,2,opt,name=file_id,json=fileId,proto3" json:"file_id,omitempty"`
	MovieId              uint32   `protobuf:"varint,3,opt,name=movie_id,json=movieId,proto3" json:"movie_id,omitempty"`
	Filename             string   `protobuf:"bytes,4,opt,name=filename,proto3" json:"filename,omitempty"`
	ServiceId            uint32   `protobuf:"varint,5,opt,name=service_id,json=serviceId,proto3" json:"service_id,omitempty"`
	XXX_NoUnkeyedLiteral struct{} `json:"-"`
	XXX_unrecognized     []byte   `json:"-"`
	XXX_sizecache        int32    `json:"-"`
}

func (m *MovieFile) Reset()         { *m = MovieFile{} }
func (m *MovieFile) String() string { return proto.CompactTextString(m) }
func (*MovieFile) ProtoMessage()    {}
func (*MovieFile) Descriptor() ([]byte, []int) {
	return fileDescriptor_546d72ade507cae9, []int{0}
}

func (m *MovieFile) XXX_Unmarshal(b []byte) error {
	return xxx_messageInfo_MovieFile.Unmarshal(m, b)
}
func (m *MovieFile) XXX_Marshal(b []byte, deterministic bool) ([]byte, error) {
	return xxx_messageInfo_MovieFile.Marshal(b, m, deterministic)
}
func (m *MovieFile) XXX_Merge(src proto.Message) {
	xxx_messageInfo_MovieFile.Merge(m, src)
}
func (m *MovieFile) XXX_Size() int {
	return xxx_messageInfo_MovieFile.Size(m)
}
func (m *MovieFile) XXX_DiscardUnknown() {
	xxx_messageInfo_MovieFile.DiscardUnknown(m)
}

var xxx_messageInfo_MovieFile proto.InternalMessageInfo

func (m *MovieFile) GetXId() string {
	if m != nil {
		return m.XId
	}
	return ""
}

func (m *MovieFile) GetFileId() uint32 {
	if m != nil {
		return m.FileId
	}
	return 0
}

func (m *MovieFile) GetMovieId() uint32 {
	if m != nil {
		return m.MovieId
	}
	return 0
}

func (m *MovieFile) GetFilename() string {
	if m != nil {
		return m.Filename
	}
	return ""
}

func (m *MovieFile) GetServiceId() uint32 {
	if m != nil {
		return m.ServiceId
	}
	return 0
}

func init() {
	proto.RegisterType((*MovieFile)(nil), "stabox.MovieFile")
}

func init() { proto.RegisterFile("movies.proto", fileDescriptor_546d72ade507cae9) }

var fileDescriptor_546d72ade507cae9 = []byte{
	// 186 bytes of a gzipped FileDescriptorProto
	0x1f, 0x8b, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0xff, 0xe2, 0xe2, 0xc9, 0xcd, 0x2f, 0xcb,
	0x4c, 0x2d, 0xd6, 0x2b, 0x28, 0xca, 0x2f, 0xc9, 0x17, 0x62, 0x2b, 0x2e, 0x49, 0x4c, 0xca, 0xaf,
	0x50, 0xea, 0x66, 0xe4, 0xe2, 0xf4, 0x05, 0x49, 0xb8, 0x65, 0xe6, 0xa4, 0x0a, 0xf1, 0x73, 0x31,
	0xc7, 0x67, 0xa6, 0x48, 0x30, 0x2a, 0x30, 0x6a, 0x70, 0x06, 0x31, 0x79, 0xa6, 0x08, 0x89, 0x73,
	0xb1, 0xa7, 0x65, 0xe6, 0xa4, 0x82, 0x04, 0x99, 0x14, 0x18, 0x35, 0x78, 0x83, 0xd8, 0x40, 0x5c,
	0xcf, 0x14, 0x21, 0x49, 0x2e, 0x0e, 0xb0, 0x79, 0x20, 0x19, 0x66, 0xb0, 0x0c, 0x3b, 0x98, 0xef,
	0x99, 0x22, 0x24, 0xc5, 0xc5, 0x01, 0x52, 0x94, 0x97, 0x98, 0x9b, 0x2a, 0xc1, 0x02, 0x36, 0x09,
	0xce, 0x17, 0x92, 0xe5, 0xe2, 0x2a, 0x4e, 0x2d, 0x2a, 0xcb, 0x4c, 0x06, 0x6b, 0x64, 0x05, 0x6b,
	0xe4, 0x84, 0x8a, 0x78, 0xa6, 0x18, 0xd9, 0x73, 0xb1, 0x81, 0x1d, 0x53, 0x2c, 0x64, 0xca, 0xc5,
	0x9d, 0x9e, 0x5a, 0x02, 0x72, 0x94, 0x67, 0x5e, 0x5a, 0xbe, 0x90, 0xa0, 0x1e, 0xc4, 0xbd, 0x7a,
	0x70, 0xb7, 0x4a, 0x61, 0x0a, 0x29, 0x31, 0x24, 0xb1, 0x81, 0x7d, 0x67, 0x0c, 0x08, 0x00, 0x00,
	0xff, 0xff, 0x8b, 0x74, 0xfa, 0x3f, 0xed, 0x00, 0x00, 0x00,
}

// Reference imports to suppress errors if they are not otherwise used.
var _ context.Context
var _ grpc.ClientConn

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
const _ = grpc.SupportPackageIsVersion4

// MoviesClient is the client API for Movies service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://godoc.org/google.golang.org/grpc#ClientConn.NewStream.
type MoviesClient interface {
	GetFileInfo(ctx context.Context, in *MovieFile, opts ...grpc.CallOption) (*MovieFile, error)
}

type moviesClient struct {
	cc *grpc.ClientConn
}

func NewMoviesClient(cc *grpc.ClientConn) MoviesClient {
	return &moviesClient{cc}
}

func (c *moviesClient) GetFileInfo(ctx context.Context, in *MovieFile, opts ...grpc.CallOption) (*MovieFile, error) {
	out := new(MovieFile)
	err := c.cc.Invoke(ctx, "/stabox.Movies/getFileInfo", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// MoviesServer is the server API for Movies service.
type MoviesServer interface {
	GetFileInfo(context.Context, *MovieFile) (*MovieFile, error)
}

// UnimplementedMoviesServer can be embedded to have forward compatible implementations.
type UnimplementedMoviesServer struct {
}

func (*UnimplementedMoviesServer) GetFileInfo(ctx context.Context, req *MovieFile) (*MovieFile, error) {
	return nil, status.Errorf(codes.Unimplemented, "method GetFileInfo not implemented")
}

func RegisterMoviesServer(s *grpc.Server, srv MoviesServer) {
	s.RegisterService(&_Movies_serviceDesc, srv)
}

func _Movies_GetFileInfo_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(MovieFile)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(MoviesServer).GetFileInfo(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/stabox.Movies/GetFileInfo",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(MoviesServer).GetFileInfo(ctx, req.(*MovieFile))
	}
	return interceptor(ctx, in, info, handler)
}

var _Movies_serviceDesc = grpc.ServiceDesc{
	ServiceName: "stabox.Movies",
	HandlerType: (*MoviesServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "getFileInfo",
			Handler:    _Movies_GetFileInfo_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "movies.proto",
}
