// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.5.1
// - protoc             v3.19.6
// source: Compiler/compiler.proto

package __

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.64.0 or later.
const _ = grpc.SupportPackageIsVersion9

const (
	CompilerService_Compile_FullMethodName = "/compiler.CompilerService/Compile"
)

// CompilerServiceClient is the client API for CompilerService service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type CompilerServiceClient interface {
	Compile(ctx context.Context, in *CompileRequest, opts ...grpc.CallOption) (*CompileResponse, error)
}

type compilerServiceClient struct {
	cc grpc.ClientConnInterface
}

func NewCompilerServiceClient(cc grpc.ClientConnInterface) CompilerServiceClient {
	return &compilerServiceClient{cc}
}

func (c *compilerServiceClient) Compile(ctx context.Context, in *CompileRequest, opts ...grpc.CallOption) (*CompileResponse, error) {
	cOpts := append([]grpc.CallOption{grpc.StaticMethod()}, opts...)
	out := new(CompileResponse)
	err := c.cc.Invoke(ctx, CompilerService_Compile_FullMethodName, in, out, cOpts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

// CompilerServiceServer is the server API for CompilerService service.
// All implementations must embed UnimplementedCompilerServiceServer
// for forward compatibility.
type CompilerServiceServer interface {
	Compile(context.Context, *CompileRequest) (*CompileResponse, error)
	mustEmbedUnimplementedCompilerServiceServer()
}

// UnimplementedCompilerServiceServer must be embedded to have
// forward compatible implementations.
//
// NOTE: this should be embedded by value instead of pointer to avoid a nil
// pointer dereference when methods are called.
type UnimplementedCompilerServiceServer struct{}

func (UnimplementedCompilerServiceServer) Compile(context.Context, *CompileRequest) (*CompileResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Compile not implemented")
}
func (UnimplementedCompilerServiceServer) mustEmbedUnimplementedCompilerServiceServer() {}
func (UnimplementedCompilerServiceServer) testEmbeddedByValue()                         {}

// UnsafeCompilerServiceServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to CompilerServiceServer will
// result in compilation errors.
type UnsafeCompilerServiceServer interface {
	mustEmbedUnimplementedCompilerServiceServer()
}

func RegisterCompilerServiceServer(s grpc.ServiceRegistrar, srv CompilerServiceServer) {
	// If the following call pancis, it indicates UnimplementedCompilerServiceServer was
	// embedded by pointer and is nil.  This will cause panics if an
	// unimplemented method is ever invoked, so we test this at initialization
	// time to prevent it from happening at runtime later due to I/O.
	if t, ok := srv.(interface{ testEmbeddedByValue() }); ok {
		t.testEmbeddedByValue()
	}
	s.RegisterService(&CompilerService_ServiceDesc, srv)
}

func _CompilerService_Compile_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(CompileRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(CompilerServiceServer).Compile(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: CompilerService_Compile_FullMethodName,
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(CompilerServiceServer).Compile(ctx, req.(*CompileRequest))
	}
	return interceptor(ctx, in, info, handler)
}

// CompilerService_ServiceDesc is the grpc.ServiceDesc for CompilerService service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var CompilerService_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "compiler.CompilerService",
	HandlerType: (*CompilerServiceServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "Compile",
			Handler:    _CompilerService_Compile_Handler,
		},
	},
	Streams:  []grpc.StreamDesc{},
	Metadata: "Compiler/compiler.proto",
}
